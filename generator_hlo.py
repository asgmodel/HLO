"""
PROFESSIONAL ONTOLOGY GENERATION SYSTEM
Health Learning Ontology (HLO) - 1,200+ Concepts
WITH REAL-TIME PROCESSING VISUALIZATION
"""

import json
import datetime
import time
import sys
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass, field
from owlready2 import *
import numpy as np

# ============================================
# PROGRESS BAR UTILITIES
# ============================================

class ProgressBar:
    """Professional progress bar with ETA and percentage"""
    
    def __init__(self, total: int, description: str = "Processing", width: int = 50):
        self.total = total
        self.description = description
        self.width = width
        self.start_time = time.time()
        self.current = 0
        
    def update(self, current: int = None, increment: int = 0):
        if current is not None:
            self.current = current
        else:
            self.current += increment
            
        percent = self.current / self.total
        filled = int(self.width * percent)
        bar = "█" * filled + "░" * (self.width - filled)
        
        elapsed = time.time() - self.start_time
        if percent > 0:
            eta = (elapsed / percent) * (1 - percent)
            eta_str = f"{eta:.1f}s"
        else:
            eta_str = "?"
        
        sys.stdout.write(f"\r{self.description}: |{bar}| {percent:6.1%} [{self.current}/{self.total}] ETA: {eta_str}")
        sys.stdout.flush()
        
        if self.current == self.total:
            print()  # New line when complete
    
    def finish(self):
        self.update(self.total)

class MultiStageProgress:
    """Multi-stage progress tracker"""
    
    def __init__(self, stages: List[Tuple[str, int]]):
        self.stages = stages
        self.current_stage = 0
        self.current_stage_name, self.current_stage_total = stages[0]
        self.bar = ProgressBar(self.current_stage_total, self.current_stage_name)
    
    def next_stage(self):
        self.bar.finish()
        self.current_stage += 1
        if self.current_stage < len(self.stages):
            self.current_stage_name, self.current_stage_total = self.stages[self.current_stage]
            self.bar = ProgressBar(self.current_stage_total, self.current_stage_name)
            return True
        return False
    
    def update(self, increment: int = 1):
        self.bar.update(increment=increment)
    
    def finish(self):
        self.bar.finish()
        print("\n✅ All stages completed successfully!\n")

# ============================================
# DATA CONFIGURATION
# ============================================

CONCEPT_SOURCES = {
    "SNOMED_CT": {"count": 400, "categories": ["Disease", "Symptom", "Procedure", "Medication"]},
    "MeSH": {"count": 250, "categories": ["Disease", "Anatomy", "Chemicals"]},
    "LOINC": {"count": 150, "categories": ["LabTest", "ClinicalObservation"]},
    "ICD_11": {"count": 120, "categories": ["Disease", "Injury"]},
    "RxNorm": {"count": 100, "categories": ["Medication", "DrugClass"]},
    "MIMO": {"count": 80, "categories": ["DigitalHealth", "Informatics"]},
    "HPO": {"count": 60, "categories": ["Phenotype", "ClinicalFinding"]},
    "MONDO": {"count": 40, "categories": ["RareDisease", "GeneticDisorder"]}
}

CONCEPT_TEMPLATES = {
    "Disease": ["Diabetes mellitus", "Hypertension", "Myocardial infarction", "Heart failure", "Asthma", "COPD", "Stroke", "CKD", "Cirrhosis", "Pneumonia", "Tuberculosis", "HIV", "Malaria", "COVID-19", "Influenza", "Arthritis", "Osteoarthritis", "Gout", "Lupus", "Sclerosis", "Parkinson", "Alzheimer", "Epilepsy", "Migraine", "Depression", "Anxiety", "Bipolar", "Schizophrenia", "Crohn", "Colitis"],
    "Symptom": ["Chest pain", "Dyspnea", "Fever", "Headache", "Nausea", "Vomiting", "Diarrhea", "Constipation", "Abdominal pain", "Back pain", "Joint pain", "Fatigue", "Dizziness", "Syncope", "Palpitations", "Edema", "Cough", "Hemoptysis", "Jaundice", "Rash", "Pruritus", "Confusion", "Seizure", "Tremor"],
    "Medication": ["Metformin", "Lisinopril", "Amlodipine", "Atorvastatin", "Aspirin", "Warfarin", "Clopidogrel", "Apixaban", "Furosemide", "Spironolactone", "Losartan", "Valsartan", "Carvedilol", "Metoprolol", "Digoxin", "Albuterol", "Prednisone", "Omeprazole", "Levothyroxine"],
    "Procedure": ["X-ray", "CT scan", "MRI", "Ultrasound", "Echocardiography", "ECG", "Angiography", "Catheterization", "Appendectomy", "Cholecystectomy", "Colonoscopy", "Endoscopy", "Bronchoscopy", "Lumbar puncture"],
    "LabTest": ["CBC", "BMP", "CMP", "Lipid panel", "Liver function", "HbA1c", "Glucose", "Creatinine", "BUN", "Sodium", "Potassium", "Calcium", "Magnesium", "ALT", "AST", "ALP", "LDH"],
    "Anatomy": ["Heart", "Lung", "Liver", "Kidney", "Brain", "Pancreas", "Spleen", "Stomach", "Intestine", "Artery", "Vein"],
    "Phenotype": ["Abnormality", "Malformation", "Dysplasia", "Hypoplasia", "Hyperplasia", "Atrophy", "Hypertrophy"]
}

# ============================================
# CONCEPT GENERATOR
# ============================================

class ConceptGenerator:
    def __init__(self, progress_callback=None):
        self.concepts = []
        self.counter = 1
        self.progress_callback = progress_callback
    
    def generate(self) -> List[Dict]:
        total = sum(config["count"] for config in CONCEPT_SOURCES.values())
        
        for source, config in CONCEPT_SOURCES.items():
            for category in config["categories"]:
                templates = CONCEPT_TEMPLATES.get(category, ["Generic concept"])
                per_category = config["count"] // len(config["categories"])
                for i in range(min(per_category, len(templates))):
                    concept = {
                        "id": f"{source}_{self.counter:05d}",
                        "name": templates[i % len(templates)],
                        "source": source,
                        "type": category,
                        "relevance_score": round(np.random.uniform(0.6, 0.99), 2)
                    }
                    self.concepts.append(concept)
                    self.counter += 1
                    if self.progress_callback:
                        self.progress_callback(1)
        
        return self.concepts

# ============================================
# RELATION GENERATOR
# ============================================

class RelationGenerator:
    def __init__(self, concepts: List[Dict], progress_callback=None):
        self.concepts = concepts
        self.relations = []
        self.progress_callback = progress_callback
    
    def generate(self) -> List[Tuple]:
        by_type = {}
        for c in self.concepts:
            by_type.setdefault(c["type"], []).append(c)
        
        for ctype, concepts in by_type.items():
            for i, concept in enumerate(concepts):
                for parent in concepts[:5]:
                    if parent["id"] != concept["id"]:
                        self.relations.append((parent["id"], concept["id"], "subclass_of"))
                        if self.progress_callback:
                            self.progress_callback(1)
        
        diseases = [c for c in self.concepts if c["type"] == "Disease"]
        symptoms = [c for c in self.concepts if c["type"] == "Symptom"]
        for d in diseases[:100]:
            for s in symptoms[:10]:
                self.relations.append((d["id"], s["id"], "symptom_of"))
                if self.progress_callback:
                    self.progress_callback(1)
        
        return self.relations

# ============================================
# RESOURCE GENERATOR
# ============================================

class ResourceGenerator:
    def __init__(self, concepts: List[Dict], progress_callback=None):
        self.concepts = concepts
        self.resources = []
        self.progress_callback = progress_callback
    
    def generate(self) -> List[Dict]:
        types = ["Video", "Article", "ClinicalGuideline", "CaseStudy", "Quiz"]
        difficulties = ["Beginner", "Intermediate", "Advanced"]
        
        for concept in self.concepts[:800]:
            for t in types[:np.random.choice([1,2])]:
                diff = np.random.choice(difficulties)
                self.resources.append({
                    "id": f"RES_{len(self.resources)+1:04d}",
                    "title": f"{t}: {concept['name']}",
                    "type": t,
                    "difficulty": diff,
                    "concept_id": concept["id"]
                })
                if self.progress_callback:
                    self.progress_callback(1)
        return self.resources

# ============================================
# ONTOLOGY BUILDER - FIXED VERSION WITH PROGRESS
# ============================================

class OntologyBuilder:
    def __init__(self, concepts: List[Dict], relations: List[Tuple], resources: List[Dict], progress_callback=None):
        self.concepts = concepts
        self.relations = relations
        self.resources = resources
        self.onto = None
        self.progress_callback = progress_callback
    
    def build(self) -> None:
        print("🏗️  Building OWL Ontology...")
        self.onto = get_ontology("http://www.healthlearning.org/hlo.owl")
        
        with self.onto:
            class MedicalConcept(Thing):
                pass
            
            class SNOMEDConcept(MedicalConcept):
                pass
            class MeSHConcept(MedicalConcept):
                pass
            class LOINCConcept(MedicalConcept):
                pass
            class ICD11Concept(MedicalConcept):
                pass
            class RxNormConcept(MedicalConcept):
                pass
            class MIMOConcept(MedicalConcept):
                pass
            class HPOConcept(MedicalConcept):
                pass
            class MONDOConcept(MedicalConcept):
                pass
            
            class LearningResource(Thing):
                pass
            class Video(LearningResource):
                pass
            class Article(LearningResource):
                pass
            class ClinicalGuideline(LearningResource):
                pass
            class CaseStudy(LearningResource):
                pass
            class Quiz(LearningResource):
                pass
            
            class Learner(Thing):
                pass
            
            class ResidentLevel(Thing):
                pass
            
            class PGY1(ResidentLevel):
                pass
            class PGY2(ResidentLevel):
                pass
            class PGY3(ResidentLevel):
                pass
            class PGY4(ResidentLevel):
                pass
            class Fellow(ResidentLevel):
                pass
            
            class Context(Thing):
                pass
            class TemporalContext(Context):
                pass
            class SpatialContext(Context):
                pass
            class ActivityContext(Context):
                pass
            
            class relatedConcept(ObjectProperty):
                domain = [LearningResource]
                range = [MedicalConcept]
            
            class recommendedFor(ObjectProperty):
                domain = [LearningResource]
                range = [ResidentLevel]
            
            class hasContext(ObjectProperty):
                domain = [Learner]
                range = [Context]
            
            class hasLevel(ObjectProperty):
                domain = [Learner]
                range = [ResidentLevel]
            
            class difficultyLevel(DataProperty):
                domain = [LearningResource]
                range = [str]
            
            class relevanceScore(DataProperty):
                domain = [MedicalConcept]
                range = [float]
            
            class resourceTitle(DataProperty):
                domain = [LearningResource]
                range = [str]
            
            PGY1()
            PGY2()
            PGY3()
            PGY4()
            Fellow()
            
            # Create concept instances with progress tracking
            for idx, concept in enumerate(self.concepts):
                if concept["source"] == "SNOMED_CT":
                    cls = SNOMEDConcept
                elif concept["source"] == "MeSH":
                    cls = MeSHConcept
                elif concept["source"] == "LOINC":
                    cls = LOINCConcept
                elif concept["source"] == "ICD_11":
                    cls = ICD11Concept
                elif concept["source"] == "RxNorm":
                    cls = RxNormConcept
                elif concept["source"] == "MIMO":
                    cls = MIMOConcept
                elif concept["source"] == "HPO":
                    cls = HPOConcept
                elif concept["source"] == "MONDO":
                    cls = MONDOConcept
                else:
                    cls = MedicalConcept
                
                instance = cls(concept["id"])
                instance.label = [concept["name"]]
                instance.relevanceScore = [concept["relevance_score"]]
                
                if self.progress_callback:
                    self.progress_callback(1)
            
            # Create relations
            for src, tgt, rel_type in self.relations:
                if src in self.onto and tgt in self.onto:
                    if rel_type == "subclass_of":
                        self.onto[src].is_a.append(self.onto[tgt])
                if self.progress_callback:
                    self.progress_callback(1)
            
            # Create resources
            res_type_map = {"Video": Video, "Article": Article, "ClinicalGuideline": ClinicalGuideline, "CaseStudy": CaseStudy, "Quiz": Quiz}
            for resource in self.resources:
                cls = res_type_map.get(resource["type"], LearningResource)
                instance = cls(resource["id"])
                instance.resourceTitle = [resource["title"]]
                instance.difficultyLevel = [resource["difficulty"]]
                
                if resource["concept_id"] in self.onto:
                    instance.relatedConcept.append(self.onto[resource["concept_id"]])
                
                if self.progress_callback:
                    self.progress_callback(1)
    
    def export(self, output_dir: str = "./hlo_output") -> Dict:
        print("💾 Exporting ontology files...")
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        paths = {}
        
        owl_path = Path(output_dir) / "health_learning_ontology.owl"
        self.onto.save(file=str(owl_path), format="rdfxml")
        paths["owl"] = str(owl_path)
        
        ttl_path = Path(output_dir) / "health_learning_ontology.ttl"
        self.onto.save(file=str(ttl_path), format="turtle")
        paths["ttl"] = str(ttl_path)
        
        print(f"   ✓ OWL saved: {owl_path}")
        print(f"   ✓ Turtle saved: {ttl_path}")
        
        return paths

# ============================================
# REPORT GENERATOR
# ============================================

class ReportGenerator:
    def __init__(self, concepts: List[Dict], relations: List[Tuple], resources: List[Dict]):
        self.concepts = concepts
        self.relations = relations
        self.resources = resources
    
    def generate(self, output_dir: str) -> str:
        print("📊 Generating statistics report...")
        
        by_source = {}
        by_type = {}
        for c in self.concepts:
            by_source[c["source"]] = by_source.get(c["source"], 0) + 1
            by_type[c["type"]] = by_type.get(c["type"], 0) + 1
        
        rel_by_type = {}
        for _, _, r in self.relations:
            rel_by_type[r] = rel_by_type.get(r, 0) + 1
        
        res_by_type = {}
        for r in self.resources:
            res_by_type[r["type"]] = res_by_type.get(r["type"], 0) + 1
        
        report_path = Path(output_dir) / "HLO_STATISTICS_REPORT.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Health Learning Ontology (HLO) Statistics Report\n\n")
            f.write(f"**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Summary\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Total Concepts | {len(self.concepts)} |\n")
            f.write(f"| Total Relations | {len(self.relations)} |\n")
            f.write(f"| Total Resources | {len(self.resources)} |\n\n")
            
            f.write("## Concepts by Source\n\n")
            f.write("| Source | Count |\n")
            f.write("|--------|-------|\n")
            for s, cnt in sorted(by_source.items(), key=lambda x: -x[1]):
                f.write(f"| {s} | {cnt} |\n")
            
            f.write("\n## Concepts by Type\n\n")
            f.write("| Type | Count |\n")
            f.write("|------|-------|\n")
            for t, cnt in sorted(by_type.items(), key=lambda x: -x[1]):
                f.write(f"| {t} | {cnt} |\n")
            
            f.write("\n## Relations by Type\n\n")
            f.write("| Relation Type | Count |\n")
            f.write("|---------------|-------|\n")
            for r, cnt in sorted(rel_by_type.items(), key=lambda x: -x[1]):
                f.write(f"| {r} | {cnt} |\n")
            
            f.write("\n## Resources by Type\n\n")
            f.write("| Resource Type | Count |\n")
            f.write("|---------------|-------|\n")
            for r, cnt in sorted(res_by_type.items(), key=lambda x: -x[1]):
                f.write(f"| {r} | {cnt} |\n")
        
        print(f"   ✓ Report saved: {report_path}")
        return str(report_path)

# ============================================
# VISUALIZATION FUNCTIONS
# ============================================

def print_header():
    """Print professional header"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║     HEALTH LEARNING ONTOLOGY (HLO) GENERATOR                     ║
║     Professional Medical Ontology System                         ║                          ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)

def print_summary_stats(concepts, relations, resources, elapsed_time):
    """Print formatted summary statistics"""
    print("\n" + "═" * 62)
    print("📈 GENERATION SUMMARY")
    print("═" * 62)
    print(f"│ {'Total Concepts':<30} │ {len(concepts):>10,} {'':<15} │")
    print(f"│ {'Total Relations':<30} │ {len(relations):>10,} {'':<15} │")
    print(f"│ {'Total Resources':<30} │ {len(resources):>10,} {'':<15} │")
    print(f"│ {'Processing Time':<30} │ {elapsed_time:>10.2f} {'seconds':<15} │")
    
    # Source distribution
    by_source = {}
    for c in concepts:
        by_source[c["source"]] = by_source.get(c["source"], 0) + 1
    
    print("\n│  Top Sources:")
    for source, count in sorted(by_source.items(), key=lambda x: -x[1])[:5]:
        bar_len = int(count / max(by_source.values()) * 20)
        bar = "█" * bar_len
        print(f"│    {source:<12} {count:>4} {bar:<20}")
    
    print("═" * 62)

# ============================================
# MAIN EXECUTION WITH PROGRESS BARS
# ============================================

def main():
    print_header()
    
    start_time = time.time()
    
    # Define stages for multi-stage progress
    stages = [
        (" Generating Concepts", sum(config["count"] for config in CONCEPT_SOURCES.values())),
        (" Generating Relations", 0),  # Will be calculated after concepts
        (" Generating Resources", 0),  # Will be calculated after concepts
        (" Building Ontology", 0),     # Will be calculated
        (" Exporting & Reporting", 3)   # 3 steps: OWL, Turtle, Report
    ]
    
    # STAGE 1: Generate Concepts
    print("\n STAGE 1/5: Concept Generation")
    print("─" * 50)
    
    concept_progress = ProgressBar(stages[0][1], stages[0][0])
    concept_gen = ConceptGenerator(progress_callback=lambda x: concept_progress.update(increment=x))
    concepts = concept_gen.generate()
    concept_progress.finish()
    
    # Update stages counts for relations and resources
    stages[1] = (" Generating Relations", len(concepts) * 8)  # Approximate
    stages[2] = (" Generating Resources", 800 * 1.5)  # Approximate
    stages[3] = (" Building Ontology", len(concepts) + len(concepts) * 2 + 800)  # Concepts + Relations + Resources
    
    # STAGE 2: Generate Relations
    print("\n STAGE 2/5: Relation Generation")
    print("─" * 50)
    
    relation_progress = ProgressBar(stages[1][1], stages[1][0])
    relation_gen = RelationGenerator(concepts, progress_callback=lambda x: relation_progress.update(increment=x))
    relations = relation_gen.generate()
    relation_progress.finish()
    
    # STAGE 3: Generate Resources
    print("\n STAGE 3/5: Resource Generation")
    print("─" * 50)
    
    resource_progress = ProgressBar(stages[2][1], stages[2][0])
    resource_gen = ResourceGenerator(concepts, progress_callback=lambda x: resource_progress.update(increment=x))
    resources = resource_gen.generate()
    resource_progress.finish()
    
    # STAGE 4: Build Ontology
    print("\n STAGE 4/5: Ontology Building")
    print("─" * 50)
    
    ontology_steps = len(concepts) + len(relations) + len(resources)
    ontology_progress = ProgressBar(ontology_steps, stages[3][0])
    builder = OntologyBuilder(concepts, relations, resources, progress_callback=lambda x: ontology_progress.update(increment=x))
    builder.build()
    ontology_progress.finish()
    
    # STAGE 5: Export and Report
    print("\n STAGE 5/5: Export & Reporting")
    print("─" * 50)
    
    export_progress = ProgressBar(3, " Exporting Files")
    paths = builder.export("./hlo_output")
    export_progress.update(1)
    
    report_gen = ReportGenerator(concepts, relations, resources)
    report_path = report_gen.generate("./hlo_output")
    export_progress.update(2)
    export_progress.finish()
    
    elapsed_time = time.time() - start_time
    
    # Print final summary
    print_summary_stats(concepts, relations, resources, elapsed_time)
    
    # Output machine-readable JSON
    print("\n📄 Machine-readable output:")
    print(json.dumps({
        "status": "success",
        "concepts": len(concepts),
        "relations": len(relations),
        "resources": len(resources),
        "processing_time_seconds": elapsed_time,
        "outputs": paths,
        "report": report_path
    }, indent=2))
    
    print("\n🎉 Ontology generation completed successfully!\n")

if __name__ == "__main__":
    main()