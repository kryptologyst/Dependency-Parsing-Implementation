#!/usr/bin/env python3
"""
Command-line demo script for Dependency Parsing Implementation
"""

import sys
import argparse
from 0107 import DependencyParser

def main():
    """Main function for command-line demo."""
    parser = argparse.ArgumentParser(description="Dependency Parsing Demo")
    parser.add_argument("text", nargs="?", help="Text to parse")
    parser.add_argument("--model", choices=["spacy", "transformers", "both"], 
                       default="spacy", help="Model to use for parsing")
    parser.add_argument("--save", action="store_true", help="Save results to database")
    parser.add_argument("--stats", action="store_true", help="Show database statistics")
    
    args = parser.parse_args()
    
    # Initialize parser
    print("🧠 Initializing dependency parser...")
    dep_parser = DependencyParser()
    
    if args.stats:
        # Show statistics
        print("\n📊 Database Statistics:")
        stats = dep_parser.get_statistics()
        print(f"Total sentences: {stats['sentence_count']}")
        print(f"Total dependencies: {stats['dependency_count']}")
        
        if stats['common_dependencies']:
            print("\nMost common dependencies:")
            for dep, count in stats['common_dependencies'][:5]:
                print(f"  {dep}: {count}")
        
        if stats['common_pos_tags']:
            print("\nMost common POS tags:")
            for pos, count in stats['common_pos_tags'][:5]:
                print(f"  {pos}: {count}")
        return
    
    # Get text to parse
    if args.text:
        text = args.text
    else:
        text = input("Enter text to parse: ")
    
    if not text.strip():
        print("❌ No text provided")
        return
    
    print(f"\n🔍 Parsing: '{text}'")
    print(f"📋 Model: {args.model}")
    
    # Parse text
    results = {}
    
    if args.model in ["spacy", "both"]:
        print("\n🌿 Using spaCy...")
        spacy_results = dep_parser.parse_with_spacy(text)
        if "error" not in spacy_results:
            results["spaCy"] = spacy_results
            print("✅ spaCy parsing completed")
        else:
            print(f"❌ spaCy error: {spacy_results['error']}")
    
    if args.model in ["transformers", "both"]:
        print("\n🤖 Using Transformers...")
        transformer_results = dep_parser.parse_with_transformers(text)
        if "error" not in transformer_results:
            results["Transformers"] = transformer_results
            print("✅ Transformer parsing completed")
        else:
            print(f"❌ Transformer error: {transformer_results['error']}")
    
    # Display results
    if results:
        print("\n📋 Parsing Results:")
        print("=" * 60)
        
        for model_name, result in results.items():
            print(f"\n🔧 Model: {model_name}")
            print("-" * 40)
            
            if "dependencies" in result:
                print(f"{'Token':<15} {'POS':<8} {'Dep':<12} {'Head':<15}")
                print("-" * 60)
                
                for dep in result["dependencies"]:
                    print(f"{dep['token']:<15} {dep['pos']:<8} {dep['dep']:<12} {dep['head']:<15}")
                
                # Show entities if available
                if "entities" in result and result["entities"]:
                    print(f"\n🏷️  Named Entities:")
                    for entity, label in result["entities"]:
                        print(f"  {entity} ({label})")
            
            elif "results" in result:
                print("Transformer results:")
                for item in result["results"]:
                    print(f"  {item}")
        
        # Save to database if requested
        if args.save:
            print("\n💾 Saving to database...")
            for model_name, result in results.items():
                sentence_id = dep_parser.save_to_database(text, result)
                print(f"✅ Saved {model_name} results (ID: {sentence_id})")
    else:
        print("❌ No parsing results available")

if __name__ == "__main__":
    main()
