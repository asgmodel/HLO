"""
PROFESSIONAL ONTOLOGY CONCEPT CONFIGURATION SYSTEM
Customize concept distribution across multiple medical ontologies
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

# ============================================
# CONFIGURATION CLASS
# ============================================

@dataclass
class OntologySourceConfig:
    """Configuration for each ontology source"""
    name: str
    total_concepts: int
    categories: List[str]
    category_distribution: Dict[str, int] = field(default_factory=dict)
    priority: int = 1
    
class OntologyConfigManager:
    """
    Manage concept allocation across ontology sources
    User can specify exact counts for each ontology
    """
    
    # Available ontology sources with default categories
    AVAILABLE_SOURCES = {
        "SNOMED_CT": {
            "default_categories": ["Disease", "Symptom", "Procedure", "Medication", "Finding", "Event"],
            "max_concepts": 2000,
            "description": "Systematized Nomenclature of Medicine - Clinical Terms"
        },
        "MeSH": {
            "default_categories": ["Disease", "Anatomy", "Chemicals", "Psychiatry", "Phenomena"],
            "max_concepts": 1000,
            "description": "Medical Subject Headings"
        },
        "LOINC": {
            "default_categories": ["LabTest", "ClinicalObservation", "Survey", "Document"],
            "max_concepts": 800,
            "description": "Logical Observation Identifiers Names and Codes"
        },
        "ICD_11": {
            "default_categories": ["Disease", "Injury", "ExternalCause", "Procedure"],
            "max_concepts": 600,
            "description": "International Classification of Diseases 11th Revision"
        },
        "ICD_10": {
            "default_categories": ["Disease", "Injury", "ExternalCause"],
            "max_concepts": 500,
            "description": "International Classification of Diseases 10th Revision"
        },
        "RxNorm": {
            "default_categories": ["Medication", "DrugClass", "Ingredient", "Brand", "ClinicalDrug"],
            "max_concepts": 600,
            "description": "Clinical Drug Terminology"
        },
        "ATC": {
            "default_categories": ["AnatomicalGroup", "TherapeuticGroup", "PharmacologicalGroup", "ChemicalGroup"],
            "max_concepts": 400,
            "description": "Anatomical Therapeutic Chemical Classification"
        },
        "MIMO": {
            "default_categories": ["DigitalHealth", "Informatics", "Education", "Policy", "Ethics"],
            "max_concepts": 300,
            "description": "Medical Informatics Multilingual Ontology"
        },
        "HPO": {
            "default_categories": ["Phenotype", "ClinicalFinding", "Abnormality", "ModeOfInheritance"],
            "max_concepts": 400,
            "description": "Human Phenotype Ontology"
        },
        "MONDO": {
            "default_categories": ["RareDisease", "GeneticDisorder", "Syndrome", "DiseaseGroup"],
            "max_concepts": 400,
            "description": "Monarch Disease Ontology"
        },
        "DOID": {
            "default_categories": ["Disease", "GeneticDisease", "InfectiousDisease", "Neoplasm"],
            "max_concepts": 350,
            "description": "Disease Ontology"
        },
        "NCIT": {
            "default_categories": ["Neoplasm", "Finding", "Therapy", "Biologic", "Chemical"],
            "max_concepts": 500,
            "description": "NCI Thesaurus"
        },
        "OMIM": {
            "default_categories": ["GeneticDisorder", "Gene", "Phenotype", "InheritancePattern"],
            "max_concepts": 300,
            "description": "Online Mendelian Inheritance in Man"
        },
        "Orphanet": {
            "default_categories": ["RareDisease", "Disorder", "GroupOfDisorders"],
            "max_concepts": 350,
            "description": "Orphanet Rare Disease Ontology"
        },
        "CPT": {
            "default_categories": ["Procedure", "Surgery", "Radiology", "Pathology", "Evaluation"],
            "max_concepts": 500,
            "description": "Current Procedural Terminology"
        },
        "Custom": {
            "default_categories": ["General", "Specialty", "Research", "Education"],
            "max_concepts": 500,
            "description": "Custom User-Defined Concepts"
        }
    }
    
    # Common concept types for all ontologies
    COMMON_TYPES = {
        "Disease": "Diseases and disorders",
        "Symptom": "Clinical symptoms and signs",
        "Symptom_Finding": "Symptoms and clinical findings",
        "Medication": "Medications and drugs",
        "Procedure": "Medical procedures",
        "LabTest": "Laboratory tests",
        "Anatomy": "Anatomical structures",
        "ClinicalFinding": "Clinical observations",
        "Phenotype": "Phenotypic abnormalities",
        "Genetics": "Genetic concepts",
        "Diagnostic": "Diagnostic methods",
        "Treatment": "Treatment modalities",
        "Prevention": "Preventive measures",
        "Prognosis": "Prognostic factors",
        "RiskFactor": "Risk factors",
        "Complication": "Complications",
        "Pharmacology": "Pharmacological concepts",
        "HealthInformatics": "Health informatics concepts",
        "DigitalHealth": "Digital health concepts",
        "Education": "Educational concepts"
    }
    
    def __init__(self, config_file: Optional[str] = None):
        self.sources = {}
        self.total_target = 0
        if config_file and Path(config_file).exists():
            self.load_config(config_file)
    
    def set_concept_count(self, source_name: str, count: int) -> None:
        """Set specific concept count for an ontology source"""
        if source_name in self.AVAILABLE_SOURCES:
            max_count = self.AVAILABLE_SOURCES[source_name]["max_concepts"]
            if count <= max_count:
                self.sources[source_name] = {
                    "count": count,
                    "categories": self.AVAILABLE_SOURCES[source_name]["default_categories"]
                }
                print(f"✅ {source_name}: {count} concepts allocated")
            else:
                print(f"⚠️ {source_name} max is {max_count}. Using {max_count}")
                self.sources[source_name] = {
                    "count": max_count,
                    "categories": self.AVAILABLE_SOURCES[source_name]["default_categories"]
                }
        else:
            print(f"❌ Unknown source: {source_name}")
    
    def set_multiple_counts(self, config: Dict[str, int]) -> None:
        """Set concept counts for multiple sources at once"""
        for source, count in config.items():
            self.set_concept_count(source, count)
        self.total_target = sum([v["count"] for v in self.sources.values()])
        print(f"\n📊 Total concepts: {self.total_target}")
    
    def set_category_distribution(self, source_name: str, distribution: Dict[str, int]) -> None:
        """Set category distribution within a source"""
        if source_name in self.sources:
            total = self.sources[source_name]["count"]
            allocated = sum(distribution.values())
            if allocated == total:
                self.sources[source_name]["categories"] = distribution
                print(f"✅ {source_name}: Categories distribution set")
            else:
                print(f"⚠️ {source_name}: Total {allocated} != {total}. Adjusting...")
                # Auto-adjust
                factor = total / allocated
                adjusted = {k: int(v * factor) for k, v in distribution.items()}
                self.sources[source_name]["categories"] = adjusted
        else:
            print(f"❌ Source {source_name} not configured. Set count first.")
    
    def load_config(self, file_path: str) -> None:
        """Load configuration from JSON file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        self.set_multiple_counts(config.get("sources", {}))
    
    def save_config(self, file_path: str) -> None:
        """Save configuration to JSON file"""
        output = {
            "total_concepts": self.total_target,
            "sources": {k: v["count"] for k, v in self.sources.items()},
            "generated": datetime.now().isoformat()
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)
        print(f"💾 Config saved to: {file_path}")
    
    def get_allocation_report(self) -> str:
        """Generate allocation report"""
        report = []
        report.append("\n" + "="*60)
        report.append("ONTOLOGY CONCEPT ALLOCATION REPORT")
        report.append("="*60)
        report.append(f"\n{'Source':<15} {'Count':<10} {'Categories':<20}")
        report.append("-"*60)
        
        for source, config in self.sources.items():
            if isinstance(config["categories"], dict):
                cat_str = f"{len(config['categories'])} categories"
            else:
                cat_str = f"{len(config['categories'])} types"
            report.append(f"{source:<15} {config['count']:<10} {cat_str:<20}")
        
        report.append("-"*60)
        report.append(f"{'TOTAL':<15} {self.total_target:<10}")
        report.append("="*60)
        
        return "\n".join(report)
    
    def display_available_sources(self) -> None:
        """Display all available ontology sources"""
        print("\n" + "="*70)
        print("AVAILABLE ONTOLOGY SOURCES")
        print("="*70)
        print(f"\n{'Source':<15} {'Max Concepts':<15} {'Description':<40}")
        print("-"*70)
        for source, info in self.AVAILABLE_SOURCES.items():
            print(f"{source:<15} {info['max_concepts']:<15} {info['description'][:38]:<40}")
        print("="*70)

# ============================================
# INTERACTIVE CONFIGURATOR
# ============================================

class InteractiveConfigurator:
    """Interactive console-based configuration"""
    
    def __init__(self):
        self.manager = OntologyConfigManager()
        self.user_config = {}
    
    def run(self) -> Dict[str, int]:
        """Run interactive configuration session"""
        print("\n" + "="*70)
        print("📋 HEALTH LEARNING ONTOLOGY - CONCEPT CONFIGURATOR")
        print("Define how many concepts from each ontology source")
        print("="*70)
        
        self.manager.display_available_sources()
        
        print("\n" + "-"*50)
        print("ENTER CONCEPT COUNTS (or press Enter to skip)")
        print("-"*50)
        
        for source in self.manager.AVAILABLE_SOURCES.keys():
            max_con = self.manager.AVAILABLE_SOURCES[source]["max_concepts"]
            default = self._get_default_count(source)
            
            while True:
                try:
                    prompt = f"  {source} (max {max_con}, default {default}): "
                    user_input = input(prompt).strip()
                    
                    if user_input == "":
                        count = default
                    else:
                        count = int(user_input)
                    
                    if 0 <= count <= max_con:
                        self.user_config[source] = count
                        break
                    else:
                        print(f"    ⚠️ Please enter a number between 0 and {max_con}")
                except ValueError:
                    print("    ⚠️ Please enter a valid number")
        
        self.manager.set_multiple_counts(self.user_config)
        
        print("\n" + "="*50)
        print("CONFIGURATION SUMMARY")
        print("="*50)
        print(self.manager.get_allocation_report())
        
        return self.user_config
    
    def _get_default_count(self, source: str) -> int:
        """Get default count based on source importance"""
        defaults = {
            "SNOMED_CT": 400,
            "MeSH": 250,
            "LOINC": 150,
            "ICD_11": 120,
            "ICD_10": 100,
            "RxNorm": 100,
            "ATC": 80,
            "MIMO": 80,
            "HPO": 60,
            "MONDO": 60,
            "DOID": 60,
            "NCIT": 50,
            "OMIM": 50,
            "Orphanet": 50,
            "CPT": 50,
            "Custom": 50
        }
        return defaults.get(source, 50)

# ============================================
# PREDEFINED CONFIGURATION TEMPLATES
# ============================================

class ConfigurationTemplates:
    """Predefined configuration templates for common use cases"""
    
    @staticmethod
    def clinical_focus() -> Dict[str, int]:
        """Clinical medicine focus - emphasis on clinical terminologies"""
        return {
            "SNOMED_CT": 500,
            "ICD_11": 200,
            "ICD_10": 150,
            "RxNorm": 150,
            "CPT": 100,
            "LOINC": 100,
            "MeSH": 100,
            "ATC": 50,
            "MIMO": 20,
            "HPO": 20,
            "MONDO": 20,
            "Custom": 50
        }
    
    @staticmethod
    def research_focus() -> Dict[str, int]:
        """Research focus - emphasis on indexing and discovery"""
        return {
            "MeSH": 400,
            "SNOMED_CT": 200,
            "LOINC": 150,
            "ICD_11": 100,
            "MONDO": 100,
            "HPO": 80,
            "DOID": 80,
            "OMIM": 80,
            "Orphanet": 80,
            "RxNorm": 50,
            "MIMO": 50,
            "Custom": 100
        }
    
    @staticmethod
    def digital_health_focus() -> Dict[str, int]:
        """Digital health focus - emphasis on informatics"""
        return {
            "MIMO": 200,
            "SNOMED_CT": 150,
            "LOINC": 150,
            "MeSH": 100,
            "ICD_11": 50,
            "RxNorm": 50,
            "HPO": 30,
            "MONDO": 30,
            "Custom": 200
        }
    
    @staticmethod
    def comprehensive() -> Dict[str, int]:
        """Comprehensive - balanced coverage across all sources"""
        return {
            "SNOMED_CT": 300,
            "MeSH": 200,
            "LOINC": 150,
            "ICD_11": 120,
            "RxNorm": 100,
            "MIMO": 80,
            "HPO": 60,
            "MONDO": 60,
            "ATC": 50,
            "CPT": 50,
            "DOID": 50,
            "OMIM": 50,
            "Orphanet": 50,
            "NCIT": 50,
            "Custom": 80
        }
    
    @staticmethod
    def light() -> Dict[str, int]:
        """Light - minimal concepts for testing"""
        return {
            "SNOMED_CT": 100,
            "MeSH": 50,
            "LOINC": 30,
            "RxNorm": 20,
            "MIMO": 10,
            "Custom": 10
        }
    
    @staticmethod
    def ultra_large() -> Dict[str, int]:
        """Ultra Large - maximum concepts (for research)"""
        return {
            "SNOMED_CT": 1500,
            "MeSH": 800,
            "LOINC": 600,
            "ICD_11": 500,
            "RxNorm": 450,
            "ATC": 350,
            "MIMO": 250,
            "HPO": 250,
            "MONDO": 250,
            "DOID": 250,
            "OMIM": 200,
            "Orphanet": 200,
            "CPT": 200,
            "NCIT": 200,
            "Custom": 200
        }

# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """Main execution with user choice"""
    
    print("\n" + "="*70)
    print("🏥 HEALTH LEARNING ONTOLOGY - CONCEPT CONFIGURATION")
    print("="*70)
    
    print("\nSelect configuration mode:")
    print("  1. Interactive configuration (manual entry)")
    print("  2. Load configuration from file")
    print("  3. Use predefined template")
    print("  4. Display all available sources")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        # Interactive configuration
        configurator = InteractiveConfigurator()
        user_config = configurator.run()
        manager = OntologyConfigManager()
        manager.set_multiple_counts(user_config)
        manager.save_config("user_ontology_config.json")
        
    elif choice == "2":
        # Load from file
        file_path = input("Enter config file path: ").strip()
        manager = OntologyConfigManager(file_path)
        print(manager.get_allocation_report())
        
    elif choice == "3":
        # Predefined templates
        print("\nAvailable templates:")
        print("  1. Clinical Focus (diagnosis, treatment, procedures)")
        print("  2. Research Focus (literature indexing, discovery)")
        print("  3. Digital Health Focus (informatics, technology)")
        print("  4. Comprehensive (balanced coverage)")
        print("  5. Light (for testing)")
        print("  6. Ultra Large (maximum concepts)")
        
        temp_choice = input("\nSelect template (1-6): ").strip()
        
        templates = {
            "1": ConfigurationTemplates.clinical_focus,
            "2": ConfigurationTemplates.research_focus,
            "3": ConfigurationTemplates.digital_health_focus,
            "4": ConfigurationTemplates.comprehensive,
            "5": ConfigurationTemplates.light,
            "6": ConfigurationTemplates.ultra_large
        }
        
        if temp_choice in templates:
            config = templates[temp_choice]()
            manager = OntologyConfigManager()
            manager.set_multiple_counts(config)
            print(manager.get_allocation_report())
            manager.save_config(f"template_{temp_choice}_config.json")
        else:
            print("Invalid choice")
            
    elif choice == "4":
        manager = OntologyConfigManager()
        manager.display_available_sources()
    
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()