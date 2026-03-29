"""
Test script to verify the RAG system works correctly
"""
from app.core.rag_system import tax_rag

def test_rag_system():
    print("Testing Advisory Board AI RAG System...")
    print("=" * 50)

    # Test queries
    test_queries = [
        "What is Section 80C and what deductions are allowed under it?",
        "How much can I claim for health insurance under Section 80D?",
        "Can I claim home loan interest as a deduction?",
        "What is the process for filing income tax return?",
        "Are donations to charity tax deductible?"
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\nTest Query {i}: {query}")
        print("-" * 40)

        # Assess risk
        risk_level = tax_rag.assess_risk(query)
        print(f"Risk Level: {risk_level}")

        # Search for relevant documents
        results = tax_rag.search(query, n_results=2)
        print(f"Found {len(results)} relevant documents")

        if results:
            print("Top result preview:")
            print(results[0]['text'][:150] + "...")

        # Generate response
        response = tax_rag.generate_response(query)
        print(f"\nAI Response:\n{response['answer']}")
        print(f"Confidence: {response['confidence']}")
        print(f"Sources cited: {len(response['sources'])}")

    print("\n" + "=" * 50)
    print("RAG System Test Complete!")

if __name__ == "__main__":
    test_rag_system()