"""
Furbish Phrase Auditor and Corrector

This script audits all Furbish phrases in responses.json for authenticity
and provides corrections based on authentic 1998 Furby vocabulary.
"""

import json
from typing import Dict, List, Tuple, Any
from furbish_reference import (
    validate_furbish_phrase, 
    get_authentic_therapeutic_phrases,
    THERAPEUTIC_FURBISH,
    INCORRECT_PHRASES
)

class FurbishAuditor:
    """Audits and corrects Furbish phrases for authenticity."""
    
    def __init__(self, responses_file_path: str):
        self.responses_file_path = responses_file_path
        self.audit_results = []
        self.corrections_made = []
        
    def load_responses(self) -> Dict[str, Any]:
        """Load the responses.json file."""
        with open(self.responses_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_responses(self, data: Dict[str, Any]) -> None:
        """Save the corrected responses back to file."""
        with open(self.responses_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def audit_category_furbish(self, category_name: str, furbish_phrases: List[List[str]]) -> List[Tuple[str, str, str, str]]:
        """
        Audit Furbish phrases in a category.
        
        Returns:
            List of tuples: (category, original_phrase, corrected_phrase, explanation)
        """
        results = []
        
        for phrase_pair in furbish_phrases:
            if len(phrase_pair) != 2:
                results.append((category_name, str(phrase_pair), str(phrase_pair), "Invalid phrase format"))
                continue
                
            furbish_phrase, english_translation = phrase_pair
            is_valid, corrected_phrase, explanation = validate_furbish_phrase(furbish_phrase)
            
            if not is_valid:
                results.append((category_name, furbish_phrase, corrected_phrase, explanation))
            else:
                results.append((category_name, furbish_phrase, furbish_phrase, "Authentic"))
                
        return results
    
    def correct_category_furbish(self, furbish_phrases: List[List[str]]) -> List[List[str]]:
        """
        Correct Furbish phrases in a category.
        
        Returns:
            Corrected list of [furbish, english] pairs
        """
        corrected_phrases = []
        
        for phrase_pair in furbish_phrases:
            if len(phrase_pair) != 2:
                corrected_phrases.append(phrase_pair)
                continue
                
            furbish_phrase, english_translation = phrase_pair
            is_valid, corrected_phrase, explanation = validate_furbish_phrase(furbish_phrase)
            
            if not is_valid:
                # Update the English translation to match the corrected Furbish
                corrected_english = self.get_corrected_translation(corrected_phrase, english_translation)
                corrected_phrases.append([corrected_phrase, corrected_english])
                self.corrections_made.append({
                    'original': furbish_phrase,
                    'corrected': corrected_phrase,
                    'original_translation': english_translation,
                    'corrected_translation': corrected_english,
                    'reason': explanation
                })
            else:
                corrected_phrases.append([furbish_phrase, english_translation])
                
        return corrected_phrases
    
    def get_corrected_translation(self, furbish_phrase: str, original_translation: str) -> str:
        """
        Get the correct English translation for an authentic Furbish phrase.
        """
        # Check if we have a direct translation
        authentic_phrases = get_authentic_therapeutic_phrases()
        if furbish_phrase in authentic_phrases:
            return authentic_phrases[furbish_phrase]
        
        # For compound phrases, try to build translation from parts
        if '-' in furbish_phrase:
            words = furbish_phrase.split('-')
            translations = []
            for word in words:
                if word in authentic_phrases:
                    translations.append(authentic_phrases[word])
            
            if translations:
                return ' '.join(translations)
        
        # Fallback to original translation if we can't determine better
        return original_translation
    
    def audit_all_furbish(self) -> Dict[str, Any]:
        """
        Audit all Furbish phrases in the responses file.
        
        Returns:
            Dictionary with audit results and statistics
        """
        data = self.load_responses()
        categories = data.get('categories', {})
        
        total_phrases = 0
        invalid_phrases = 0
        
        for category_name, category_data in categories.items():
            furbish_phrases = category_data.get('furbish_phrases', [])
            total_phrases += len(furbish_phrases)
            
            category_results = self.audit_category_furbish(category_name, furbish_phrases)
            self.audit_results.extend(category_results)
            
            # Count invalid phrases
            invalid_phrases += sum(1 for result in category_results if result[3] != "Authentic")
        
        return {
            'total_phrases': total_phrases,
            'invalid_phrases': invalid_phrases,
            'valid_phrases': total_phrases - invalid_phrases,
            'accuracy_percentage': ((total_phrases - invalid_phrases) / total_phrases * 100) if total_phrases > 0 else 0,
            'detailed_results': self.audit_results
        }
    
    def correct_all_furbish(self) -> Dict[str, Any]:
        """
        Correct all Furbish phrases in the responses file.
        
        Returns:
            Dictionary with correction results and updated data
        """
        data = self.load_responses()
        categories = data.get('categories', {})
        
        for category_name, category_data in categories.items():
            if 'furbish_phrases' in category_data:
                corrected_phrases = self.correct_category_furbish(category_data['furbish_phrases'])
                category_data['furbish_phrases'] = corrected_phrases
        
        return data
    
    def generate_audit_report(self) -> str:
        """Generate a detailed audit report."""
        audit_results = self.audit_all_furbish()
        
        report = []
        report.append("=" * 60)
        report.append("FURBISH AUTHENTICITY AUDIT REPORT")
        report.append("=" * 60)
        report.append("")
        
        report.append(f"Total Furbish phrases analyzed: {audit_results['total_phrases']}")
        report.append(f"Authentic phrases: {audit_results['valid_phrases']}")
        report.append(f"Non-authentic phrases: {audit_results['invalid_phrases']}")
        report.append(f"Authenticity rate: {audit_results['accuracy_percentage']:.1f}%")
        report.append("")
        
        if audit_results['invalid_phrases'] > 0:
            report.append("DETAILED FINDINGS:")
            report.append("-" * 40)
            
            for category, original, corrected, explanation in audit_results['detailed_results']:
                if explanation != "Authentic":
                    report.append(f"Category: {category}")
                    report.append(f"  Original: {original}")
                    report.append(f"  Corrected: {corrected}")
                    report.append(f"  Reason: {explanation}")
                    report.append("")
        
        return "\n".join(report)
    
    def apply_corrections_and_save(self) -> str:
        """Apply all corrections and save the updated file."""
        corrected_data = self.correct_all_furbish()
        self.save_responses(corrected_data)
        
        report = []
        report.append("CORRECTIONS APPLIED:")
        report.append("-" * 30)
        
        if not self.corrections_made:
            report.append("No corrections needed - all phrases were already authentic!")
        else:
            for correction in self.corrections_made:
                report.append(f"'{correction['original']}' -> '{correction['corrected']}'")
                report.append(f"  Translation: '{correction['original_translation']}' -> '{correction['corrected_translation']}'")
                report.append(f"  Reason: {correction['reason']}")
                report.append("")
        
        return "\n".join(report)

def main():
    """Main function to run the audit and correction process."""
    auditor = FurbishAuditor('furby_therapist/responses.json')
    
    print("Generating audit report...")
    audit_report = auditor.generate_audit_report()
    print(audit_report)
    
    print("\nApplying corrections...")
    correction_report = auditor.apply_corrections_and_save()
    print(correction_report)
    
    print("\nFurbish authenticity audit and correction complete!")

if __name__ == "__main__":
    main()