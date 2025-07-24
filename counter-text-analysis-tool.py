# Problem: Create a text analysis tool that provides comprehensive statistics about text content, useful for content writers and SEO analysis.

# Task: Implement a TextAnalyzer class using Counter for various text statistics.

from collections import Counter
import re

class TextAnalyzer:
    def __init__(self, text):
        """
        Initialize with text to analyze
        Args:
            text (str): Text to analyze
        """
        self.original_text = text
        self.text = text.lower()  # For case-insensitive analysis
    
    def get_character_frequency(self, include_spaces=False):
        """
        Get frequency of each character
        Args:
            include_spaces (bool): Whether to include spaces in count
        Returns:
            Counter: Character frequencies
        """
        if include_spaces:
            return Counter(self.text)
        else:
            return Counter(char for char in self.text if not char.isspace())
    
    def get_word_frequency(self, min_length=1):
        """
        Get frequency of each word (minimum length filter)
        Args:
            min_length (int): Minimum word length to include
        Returns:
            Counter: Word frequencies
        """
        # Extract words using regex (letters only)
        words = re.findall(r'\b[a-zA-Z]+\b', self.text)
        return Counter(word for word in words if len(word) >= min_length)
    
    def get_sentence_length_distribution(self):
        """
        Analyze sentence lengths (in words)
        Returns:
            dict: Contains 'lengths' (Counter), 'average', 'longest', 'shortest'
        """
        # Split by sentence endings
        sentences = re.split(r'[.!?]+', self.original_text)
        sentence_lengths = []
        
        for sentence in sentences:
            words = re.findall(r'\b\w+\b', sentence.strip())
            if words:  # Only count non-empty sentences
                sentence_lengths.append(len(words))
        
        if not sentence_lengths:
            return {'lengths': Counter(), 'average': 0, 'longest': 0, 'shortest': 0}
        
        lengths_counter = Counter(sentence_lengths)
        return {
            'lengths': lengths_counter,
            'average': sum(sentence_lengths) / len(sentence_lengths),
            'longest': max(sentence_lengths),
            'shortest': min(sentence_lengths)
        }
    
    def find_common_words(self, n=10, exclude_common=True):
        """
        Find most common words, optionally excluding very common English words
        Args:
            n (int): Number of words to return
            exclude_common (bool): Exclude common words like 'the', 'and', etc.
        Returns:
            list: List of tuples (word, count)
        """
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
                       'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                       'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
                       'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        
        word_freq = self.get_word_frequency()
        
        if exclude_common:
            filtered_freq = Counter({word: count for word, count in word_freq.items() 
                                   if word not in common_words})
            return filtered_freq.most_common(n)
        else:
            return word_freq.most_common(n)
    
    def get_reading_statistics(self):
        """
        Get comprehensive reading statistics
        Returns:
            dict: Contains character_count, word_count, sentence_count,
                  average_word_length, reading_time_minutes (assume 200 WPM)
        """
        words = re.findall(r'\b\w+\b', self.original_text)
        sentences = re.split(r'[.!?]+', self.original_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        word_lengths = [len(word) for word in words]
        avg_word_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0
        
        # Estimate reading time (200 words per minute)
        reading_time = len(words) / 200 if words else 0
        
        return {
            'character_count': len(self.original_text),
            'word_count': len(words),
            'sentence_count': len(sentences),
            'average_word_length': round(avg_word_length, 2),
            'reading_time_minutes': round(reading_time, 2)
        }
    
    def compare_with_text(self, other_text):
        """
        Compare this text with another text
        Args:
            other_text (str): Text to compare with
        Returns:
            dict: Contains 'common_words', 'similarity_score', 'unique_to_first', 'unique_to_second'
        """
        other_analyzer = TextAnalyzer(other_text)
        
        words1 = set(self.get_word_frequency().keys())
        words2 = set(other_analyzer.get_word_frequency().keys())
        
        common_words = words1.intersection(words2)
        unique_to_first = words1 - words2
        unique_to_second = words2 - words1
        
        # Simple similarity score based on common words
        total_unique_words = len(words1.union(words2))
        similarity_score = len(common_words) / total_unique_words if total_unique_words > 0 else 0
        
        return {
            'common_words': len(common_words),
            'similarity_score': round(similarity_score, 3),
            'unique_to_first': len(unique_to_first),
            'unique_to_second': len(unique_to_second)
        }


# Test your implementation
sample_text = """
Python is a high-level, interpreted programming language with dynamic semantics.
Its high-level built-in data structures, combined with dynamic typing and dynamic binding,
make it very attractive for Rapid Application Development. Python is simple, easy to learn
syntax emphasizes readability and therefore reduces the cost of program maintenance.
Python supports modules and packages, which encourages program modularity and code reuse.
The Python interpreter and the extensive standard library are available in source or binary
form without charge for all major platforms, and can be freely distributed.
"""

analyzer = TextAnalyzer(sample_text)

print("Character frequency (top 5):", analyzer.get_character_frequency().most_common(5))
print("Word frequency (top 5):", analyzer.get_word_frequency().most_common(5))
print("Common words:", analyzer.find_common_words(5))
print("Reading statistics:", analyzer.get_reading_statistics())

# Compare with another text
other_text = "Java is a programming language. Java is object-oriented and platform independent."
comparison = analyzer.compare_with_text(other_text)
print("Comparison results:", comparison)