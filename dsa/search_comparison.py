"""
Data Structures & Algorithms - Search Comparison
Implements and compares Linear Search vs Dictionary Lookup
Author: Person 1
"""

import time
import json
from xml_parser import parse_xml_to_json


class SearchComparison:
    """Class to compare different search algorithms"""
    
    def __init__(self, transactions):
        """
        Initialize with transaction data
        
        Args:
            transactions (list): List of transaction dictionaries
        """
        self.transactions_list = transactions
        self.transactions_dict = {trans['id']: trans for trans in transactions}
    
    def linear_search(self, transaction_id):
        """
        Linear Search - O(n) time complexity
        Scans through the entire list to find a transaction by ID
        
        Args:
            transaction_id (int): ID of transaction to find
            
        Returns:
            dict or None: Transaction if found, None otherwise
        """
        for transaction in self.transactions_list:
            if transaction['id'] == transaction_id:
                return transaction
        return None
    
    def dictionary_lookup(self, transaction_id):
        """
        Dictionary Lookup - O(1) time complexity
        Uses hash table for constant time lookup
        
        Args:
            transaction_id (int): ID of transaction to find
            
        Returns:
            dict or None: Transaction if found, None otherwise
        """
        return self.transactions_dict.get(transaction_id)
    
    def measure_search_time(self, search_function, transaction_id, iterations=1000):
        """
        Measure average search time for a given function
        
        Args:
            search_function: Function to measure
            transaction_id (int): ID to search for
            iterations (int): Number of iterations to average
            
        Returns:
            float: Average time in microseconds
        """
        start_time = time.perf_counter()
        
        for _ in range(iterations):
            search_function(transaction_id)
        
        end_time = time.perf_counter()
        avg_time = (end_time - start_time) / iterations * 1_000_000  # Convert to microseconds
        
        return avg_time
    
    def compare_searches(self, test_ids):
        """
        Compare linear search vs dictionary lookup performance
        
        Args:
            test_ids (list): List of transaction IDs to test
            
        Returns:
            dict: Comparison results
        """
        results = {
            'linear_search_times': [],
            'dictionary_lookup_times': [],
            'test_ids': test_ids
        }
        
        print("=" * 70)
        print("SEARCH ALGORITHM PERFORMANCE COMPARISON")
        print("=" * 70)
        print(f"Dataset size: {len(self.transactions_list)} transactions")
        print(f"Testing {len(test_ids)} different IDs\n")
        
        for test_id in test_ids:
            # Measure linear search
            linear_time = self.measure_search_time(self.linear_search, test_id)
            results['linear_search_times'].append(linear_time)
            
            # Measure dictionary lookup
            dict_time = self.measure_search_time(self.dictionary_lookup, test_id)
            results['dictionary_lookup_times'].append(dict_time)
            
            speedup = linear_time / dict_time if dict_time > 0 else 0
            
            print(f"Transaction ID: {test_id}")
            print(f"  Linear Search:      {linear_time:.4f} μs")
            print(f"  Dictionary Lookup:  {dict_time:.4f} μs")
            print(f"  Speedup:            {speedup:.2f}x faster")
            print("-" * 70)
        
        # Calculate averages
        avg_linear = sum(results['linear_search_times']) / len(results['linear_search_times'])
        avg_dict = sum(results['dictionary_lookup_times']) / len(results['dictionary_lookup_times'])
        
        print(f"\nAVERAGE RESULTS:")
        print(f"  Linear Search:      {avg_linear:.4f} μs")
        print(f"  Dictionary Lookup:  {avg_dict:.4f} μs")
        print(f"  Average Speedup:    {avg_linear/avg_dict:.2f}x faster")
        print("=" * 70)
        
        results['avg_linear'] = avg_linear
        results['avg_dict'] = avg_dict
        
        return results


def generate_performance_report(results):
    """
    Generate a detailed performance report
    
    Args:
        results (dict): Results from comparison
        
    Returns:
        str: Formatted report
    """
    report = """
PERFORMANCE ANALYSIS REPORT
===========================

1. LINEAR SEARCH (O(n) complexity)
   - Algorithm: Sequentially scans through all records
   - Worst case: Checks every element in the list
   - Average time: {:.4f} microseconds
   
2. DICTIONARY LOOKUP (O(1) complexity)
   - Algorithm: Uses hash table for direct access
   - Worst case: Constant time regardless of data size
   - Average time: {:.4f} microseconds

3. COMPARISON RESULTS
   - Dictionary lookup is {:.2f}x faster on average
   - For a dataset of this size, the difference is significant
   
4. WHY IS DICTIONARY LOOKUP FASTER?
   
   Linear Search:
   - Must check each element sequentially
   - Time grows linearly with data size (O(n))
   - If target is at end, checks all n elements
   
   Dictionary Lookup:
   - Uses hash function to compute key location
   - Direct access to value in constant time (O(1))
   - Performance doesn't degrade with more data
   
5. OTHER EFFICIENT DATA STRUCTURES/ALGORITHMS
   
   a) Binary Search Tree (BST)
      - Time complexity: O(log n)
      - Maintains sorted order
      - Good for range queries
   
   b) Hash Table with Chaining
      - Similar to dict but handles collisions better
      - O(1) average case
   
   c) Trie (Prefix Tree)
      - Excellent for string searches
      - O(m) where m is key length
   
   d) B-Tree / B+ Tree
      - Used in databases
      - Efficient for disk-based storage
      - O(log n) complexity
   
6. RECOMMENDATION FOR MOMO API
   - Dictionary/Hash Table is optimal for ID-based lookups
   - For complex queries (date range, amount filters), consider:
     * Indexing on frequently queried fields
     * Database with proper indexes (PostgreSQL, MongoDB)
     * Caching layer (Redis) for frequent queries

""".format(
        results['avg_linear'],
        results['avg_dict'],
        results['avg_linear'] / results['avg_dict']
    )
    
    return report


if __name__ == "__main__":
    # Parse XML data
    print("Loading transaction data...")
    transactions = parse_xml_to_json('../modified_sms_v2.xml')
    
    if not transactions:
        print("Error: No transactions loaded")
        exit(1)
    
    # Create search comparison object
    searcher = SearchComparison(transactions)
    
    # Test with multiple IDs (including edge cases)
    test_ids = [1, 5, 10, 15, 20, 22]  # First, middle, last, and some in between
    
    # Run comparison
    results = searcher.compare_searches(test_ids)
    
    # Generate and display report
    report = generate_performance_report(results)
    print("\n" + report)
    
    # Save results to JSON
    with open('search_comparison_results.json', 'w') as f:
        json.dump(results, f, indent=4)
    
    print("Results saved to search_comparison_results.json")
    
    # Save report to text file
    with open('dsa_performance_report.txt', 'w') as f:
        f.write(report)
    
    print("Report saved to dsa_performance_report.txt")
