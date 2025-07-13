"""
Pidgin Response Processor - Enhances responses with authentic Hawaiian Pidgin English
"""
import logging
import random
import re
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


class PidginResponseProcessor:
    """Processes responses to include authentic Hawaiian Pidgin English"""
    
    def __init__(self):
        # Common pidgin replacements (standard -> pidgin)
        self.pidgin_replacements = {
            # Basic replacements
            "yes": ["yeah", "yah", "rajah"],
            "no": ["nah", "no way", "no can"],
            "okay": ["k den", "shoots", "rajah dat"],
            "good": ["good", "cherry", "solid"],
            "very": ["real", "plenty", "choke"],
            "many": ["choke", "plenty", "lot of"],
            "friend": ["brah", "bruddah", "cuz"],
            "person": ["guy", "buggah", "one"],
            
            # Phrase replacements
            "how are you": ["how you stay", "howzit"],
            "what's up": ["wassup", "howzit going"],
            "let's go": ["we go", "shoots let's go"],
            "come here": ["come", "come ova here"],
            "over there": ["ova dea", "dat side"],
            "do you want": ["you like", "you want"],
            "thank you": ["mahalo", "tanks", "thank you"],
            "you're welcome": ["no worries", "no problem", "all good"],
            
            # Business-specific
            "meeting": ["meeting", "talk story session"],
            "discuss": ["talk story about", "go over"],
            "analyze": ["check out", "look at"],
            "implement": ["make happen", "set up"],
            "optimize": ["make better", "improve"],
            "solution": ["answer", "way for fix"],
            "challenge": ["problem", "tough one"],
            "opportunity": ["chance", "good opportunity"]
        }
        
        # Common pidgin expressions to sprinkle in
        self.pidgin_expressions = {
            "agreement": ["Shoots!", "Rajah!", "Can!", "Sounds good!", "K den!"],
            "emphasis": ["Fo real!", "No joke!", "Serious kine!", "Da kine!"],
            "understanding": ["I get it", "Make sense", "I understand", "Got it"],
            "excitement": ["Ho brah!", "Cheee!", "Unreal!", "So good!"],
            "concern": ["No worries", "All good", "We handle", "Can fix"],
            "transition": ["So yeah", "Anyways", "But yeah", "So den"]
        }
        
        # Pidgin sentence starters
        self.pidgin_starters = [
            "Eh, ",
            "Ho, ",
            "So, ",
            "K so, ",
            "Yeah so, ",
            "Shoots, "
        ]
        
        # Pidgin sentence endings
        self.pidgin_endings = [
            ", yeah?",
            ", you know?",
            ", das why.",
            ", for real.",
            ", can.",
            ", no worries."
        ]
        
        logger.info("Pidgin Response Processor initialized")
    
    def enhance_response(self, response: str, intensity: str = "medium") -> str:
        """
        Enhance response with Hawaiian Pidgin English
        
        Args:
            response: Original response text
            intensity: Level of pidgin to apply (light, medium, heavy)
        
        Returns:
            Enhanced response with pidgin elements
        """
        
        # First remove any bracket content (internal notes/context)
        response = self._remove_bracket_content(response)
        
        # Preserve professional terms and company names
        protected_terms = self._extract_protected_terms(response)
        
        # Apply pidgin enhancements based on intensity
        if intensity == "light":
            enhanced = self._apply_light_pidgin(response)
        elif intensity == "heavy":
            enhanced = self._apply_heavy_pidgin(response)
        else:  # medium
            enhanced = self._apply_medium_pidgin(response)
        
        # Restore protected terms
        enhanced = self._restore_protected_terms(enhanced, protected_terms)
        
        # Ensure proper capitalization and punctuation
        enhanced = self._clean_response(enhanced)
        
        return enhanced
    
    def _apply_light_pidgin(self, text: str) -> str:
        """Apply light pidgin - just a few local touches"""
        # Add occasional pidgin expressions
        sentences = text.split('. ')
        
        # Add starter to first sentence occasionally
        if random.random() < 0.3:
            sentences[0] = random.choice(self.pidgin_starters) + sentences[0].lower()
        
        # Add ending to last sentence occasionally
        if random.random() < 0.3 and len(sentences) > 1:
            sentences[-1] = sentences[-1].rstrip('.') + random.choice(self.pidgin_endings)
        
        # Replace a few key phrases
        result = '. '.join(sentences)
        for standard, pidgin_options in list(self.pidgin_replacements.items())[:5]:
            if standard in result.lower():
                result = re.sub(
                    r'\b' + standard + r'\b',
                    random.choice(pidgin_options),
                    result,
                    count=1,
                    flags=re.IGNORECASE
                )
        
        return result
    
    def _apply_medium_pidgin(self, text: str) -> str:
        """Apply medium pidgin - balanced local style"""
        sentences = text.split('. ')
        enhanced_sentences = []
        
        for i, sentence in enumerate(sentences):
            # Add starters more frequently
            if random.random() < 0.5 and i == 0:
                sentence = random.choice(self.pidgin_starters) + sentence.lower()
            
            # Apply replacements
            for standard, pidgin_options in self.pidgin_replacements.items():
                if random.random() < 0.4 and standard in sentence.lower():
                    sentence = re.sub(
                        r'\b' + standard + r'\b',
                        random.choice(pidgin_options),
                        sentence,
                        count=1,
                        flags=re.IGNORECASE
                    )
            
            # Add expressions between sentences
            if random.random() < 0.3 and i < len(sentences) - 1:
                expression_type = random.choice(list(self.pidgin_expressions.keys()))
                expression = random.choice(self.pidgin_expressions[expression_type])
                sentence += f". {expression}"
            
            enhanced_sentences.append(sentence)
        
        result = '. '.join(enhanced_sentences)
        
        # Add ending occasionally
        if random.random() < 0.4:
            result = result.rstrip('.') + random.choice(self.pidgin_endings)
        
        return result
    
    def _apply_heavy_pidgin(self, text: str) -> str:
        """Apply heavy pidgin - full local style"""
        # This would be used sparingly, mainly for very casual contexts
        result = text
        
        # Apply most replacements
        for standard, pidgin_options in self.pidgin_replacements.items():
            if standard in result.lower():
                result = re.sub(
                    r'\b' + standard + r'\b',
                    random.choice(pidgin_options),
                    result,
                    flags=re.IGNORECASE
                )
        
        # Add more expressions
        sentences = result.split('. ')
        enhanced_sentences = []
        
        for i, sentence in enumerate(sentences):
            if random.random() < 0.7:
                sentence = random.choice(self.pidgin_starters) + sentence.lower()
            
            if random.random() < 0.5:
                expression_type = random.choice(list(self.pidgin_expressions.keys()))
                expression = random.choice(self.pidgin_expressions[expression_type])
                sentence += f" {expression}"
            
            enhanced_sentences.append(sentence)
        
        return '. '.join(enhanced_sentences)
    
    def _extract_protected_terms(self, text: str) -> List[Tuple[str, str]]:
        """Extract terms that should not be modified"""
        protected = []
        
        # Protect company names
        company_patterns = [
            r'LeniLani\s+Consulting',
            r'LeniLani',
            r'HubSpot',
            r'Google\s+Calendar',
            r'Anthropic',
            r'Claude'
        ]
        
        for pattern in company_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                placeholder = f"__PROTECTED_{len(protected)}__"
                protected.append((placeholder, match.group()))
        
        # Protect technical terms
        tech_patterns = [
            r'AI|A\.I\.',
            r'API',
            r'IoT',
            r'CRM',
            r'ROI',
            r'SaaS',
            r'URL',
            r'FAQ'
        ]
        
        for pattern in tech_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                placeholder = f"__TECH_{len(protected)}__"
                protected.append((placeholder, match.group()))
        
        return protected
    
    def _restore_protected_terms(self, text: str, protected_terms: List[Tuple[str, str]]) -> str:
        """Restore protected terms to the text"""
        result = text
        for placeholder, original in protected_terms:
            result = result.replace(placeholder, original)
        return result
    
    def _clean_response(self, text: str) -> str:
        """Clean up the response for proper formatting"""
        # Fix spacing issues
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\s+\.', '.', text)
        text = re.sub(r'\s+,', ',', text)
        
        # Ensure proper sentence capitalization
        sentences = text.split('. ')
        cleaned_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                # Capitalize first letter unless it starts with a pidgin expression
                if not any(sentence.lower().startswith(starter.lower()) for starter in self.pidgin_starters):
                    sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()
                cleaned_sentences.append(sentence)
        
        return '. '.join(cleaned_sentences)
    
    def add_cultural_flavor(self, text: str, context: Dict[str, any] = None) -> str:
        """Add cultural flavor based on context"""
        if not context:
            return text
        
        # Add island-specific touches
        if "island" in context:
            island = context["island"].lower()
            island_expressions = {
                "oahu": ["town side", "country side", "da city"],
                "maui": ["up country", "west side", "south shore"],
                "big island": ["hilo side", "kona side", "puna side"],
                "kauai": ["north shore", "south shore", "east side"]
            }
            
            if island in island_expressions and random.random() < 0.3:
                expression = random.choice(island_expressions[island])
                text += f" You know how it is on {expression}!"
        
        # Add business-specific touches
        if "business_type" in context:
            business = context["business_type"].lower()
            if business == "restaurant" and random.random() < 0.3:
                text += " Da grindz going be good!"
            elif business == "tourism" and random.random() < 0.3:
                text += " Visitors going love it!"
            elif business == "agriculture" and random.random() < 0.3:
                text += " Da 'aina going thrive!"
        
        return text
    
    def _remove_bracket_content(self, text: str) -> str:
        """Remove bracket content like [Context: ...] and internal notes from the response"""
        import re
        # Remove content in square brackets (including nested brackets)
        while '[' in text and ']' in text:
            text = re.sub(r'\[[^\]]*\]', '', text)
        
        # Remove long parenthetical content (likely internal notes) 
        text = re.sub(r'\([^)]{30,}\)', '', text)
        
        # Remove common internal note patterns
        text = re.sub(r'\s*-\s*[A-Z][^.]*$', '', text)  # Remove trailing dash notes
        text = re.sub(r'Note:.*?(?=\.|$)', '', text, flags=re.IGNORECASE)
        
        # Clean up extra spaces and punctuation
        text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single
        text = re.sub(r'\s*,\s*\.', '.', text)  # Fix comma before period
        text = re.sub(r'\s*\.\s*,', '.', text)  # Fix period before comma
        text = re.sub(r'\.\s*,\s*', '. ', text)  # Fix period comma combination
        text = re.sub(r'\s*\.\s*$', '.', text)  # Clean ending
        
        return text.strip()