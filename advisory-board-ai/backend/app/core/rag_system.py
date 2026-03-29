import os
import hashlib
from typing import List, Dict, Any, Optional
import logging

# Optional heavy deps; fall back gracefully if missing for demo mode
try:
    import chromadb
    from chromadb.config import Settings
    HAS_CHROMA = True
except Exception:
    chromadb = None
    Settings = None
    HAS_CHROMA = False

try:
    from sentence_transformers import SentenceTransformer
    HAS_EMBED = True
except Exception:
    SentenceTransformer = None
    HAS_EMBED = False

try:
    import PyPDF2
except Exception:
    PyPDF2 = None

try:
    import pdfplumber
except Exception:
    pdfplumber = None

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.schema import Document
    HAS_LANGCHAIN = True
except Exception:
    RecursiveCharacterTextSplitter = None
    Document = None
    HAS_LANGCHAIN = False

logger = logging.getLogger(__name__)

class TaxRAGSystem:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2') if HAS_EMBED else None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        ) if HAS_LANGCHAIN else None

        self.collection = None
        if HAS_CHROMA:
            self.chroma_client = chromadb.PersistentClient(path=persist_directory)
            self.collection_name = "tax_act"
            try:
                self.collection = self.chroma_client.get_collection(name=self.collection_name)
                logger.info(f"Loaded existing collection: {self.collection_name}")
            except Exception:
                self.collection = self.chroma_client.create_collection(name=self.collection_name)
                logger.info(f"Created new collection: {self.collection_name}")
        else:
            logger.warning("ChromaDB not installed; running RAG in lightweight demo mode.")

    def load_tax_act(self, file_path: str) -> List[Document]:
        """Load and chunk the Income Tax Act document."""
        documents = []

        # Try different methods to extract text
        text = ""
        try:
            if pdfplumber:
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        text += (page.extract_text() or "") + "\n"
            elif PyPDF2:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += (page.extract_text() or "") + "\n"
        except Exception as e:
            logger.warning(f"PDF extraction failed: {e}")

        if not text.strip():
            logger.info("Using built-in sample tax act content")
            text = self._create_sample_tax_act()

        if not self.text_splitter or not Document:
            # Fallback: single chunk Document
            return [Document(page_content=text, metadata={"source": file_path})] if Document else []

        chunks = self.text_splitter.split_text(text)

        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
                metadata={
                    "source": file_path,
                    "chunk_id": i,
                    "total_chunks": len(chunks)
                }
            )
            documents.append(doc)

        return documents

    def _create_sample_tax_act(self) -> str:
        """Create a sample tax act for demonstration purposes."""
        return """
        INCOME TAX ACT, 1961

        SECTION 80C: Deduction in respect of life insurance premia, deferred annuity, contributions to provident fund, subscription to certain equity shares or debentures, etc.
        (1) In computing the total income of an assessee, there shall be deducted, in accordance with and subject to the provisions of this section, the whole of the amount paid or deposited in the previous year by the assessee—
        (a) to effect or keep in force an insurance on his own life or on the life of his spouse or any child of such person;
        (b) to a contract for a deferred annuity, on his own life or on the life of his spouse or any child of such person, making provision for the payment of an annuity on the date specified therein, whether or not such date is after the date of his attaining the age of sixty years;
        (c) any sum deducted from the salary payable to an employee thereof, referred to in section 80CCA, as his contribution to any recognised provident fund, to the extent it does not exceed fifteen per cent of his salary;
        (d) any sum paid by the assessee as his contribution to a recognised provident fund or to a recognised superannuation fund, by way of compulsory or voluntary contribution;
        (e) any sum paid by the assessee by way of subscription to any such security of the Central Government as the Board may, by notification in the Official Gazette, specify in this behalf;
        (f) any sum paid by the assessee by way of deposit in an account under the Post Office Savings Bank Rules, 1959, as amended from time to time, if such deposit is made on or after the 1st day of April, 2005;
        (g) any sum paid by the assessee by way of subscription to any deposit scheme of the Central Government or for any such purpose as the Board may, by notification in the Official Gazette, specify in this behalf;
        (h) any sum paid by the assessee by way of tuition fees (excluding any payment towards any development fees or donation or payment of similar nature), whether at the time of admission or thereafter, to any university, college, school or other educational institution situated within India for the purpose of full-time education of any two children of the assessee;
        (i) any sum paid by the assessee by way of payment towards the cost of purchase or construction of a residential house property the completion of which is certified by the prescribed authority;
        (j) any sum paid by the assessee by way of subscription to the equity shares or debentures of any public company or private company which is engaged in providing infrastructure facilities as approved by the Board and notified in the Official Gazette in this behalf;
        (k) any sum paid by the assessee by way of deposit for a period of five years or above with an association which is a company registered under the Companies Act, 1956 and having the main object of carrying on the business of providing infrastructure facilities;
        (l) any sum paid by the assessee by way of tuition fees, whether at the time of admission or thereafter, to any university, college, school or other educational institution situated within India for the purpose of full-time education of any two children of the assessee;
        (m) any sum paid by the assessee by way of subscription to any deposit scheme or to any such purpose as the Board may, by notification in the Official Gazette, specify in this behalf;
        (n) any sum paid by the assessee by way of deposit for a fixed period of not less than five years with a scheduled bank, in accordance with any scheme framed by the Central Government and notified in the Official Gazette in this behalf;
        (o) any sum paid by the assessee by way of deposit for a fixed period of not less than five years with the Post Office, in accordance with any scheme framed by the Central Government and notified in the Official Gazette in this behalf;
        (p) any sum paid by the assessee by way of subscription to any deposit scheme of the National Housing Bank, in accordance with any scheme framed by the Central Government and notified in the Official Gazette in this behalf;
        (q) any sum paid by the assessee by way of tuition fees, whether at the time of admission or thereafter, to any university, college, school or other educational institution situated within India for the purpose of full-time education of any two children of the assessee;
        (r) any sum paid by the assessee by way of subscription to any deposit scheme or to any such purpose as the Board may, by notification in the Official Gazette, specify in this behalf;
        (s) any sum paid by the assessee by way of subscription to any deposit scheme or to any such purpose as the Board may, by notification in the Official Gazette, specify in this behalf;
        (t) any sum paid by the assessee by way of subscription to any deposit scheme or to any such purpose as the Board may, by notification in the Official Gazette, specify in this behalf;

        SECTION 80D: Deduction in respect of health insurance premia.
        (1) In computing the total income of an assessee, there shall be deducted, in accordance with and subject to the provisions of this section, the whole of the amount paid during the previous year by the assessee—
        (a) to effect or keep in force an insurance on the health of his own self or on the health of his spouse or any dependent child or parents of such person; or
        (b) to make any payment towards the cost of purchase of any medical insurance policy for his parents.

        SECTION 24: Deduction from income from house property.
        (1) In computing the income chargeable under the head "Income from house property", there shall be allowed the following deductions, namely:—
        (a) a sum equal to thirty per cent of the annual value; and
        (b) where the property has been acquired, constructed, repaired, renewed or reconstructed with borrowed capital, the amount of any interest payable on such borrowed capital.

        SECTION 10: Incomes not forming part of total income.
        (1) The following incomes shall not form part of the total income of an assessee, unless otherwise provided in this Act, namely:—
        (a) agricultural income;
        (b) [Omitted by the Finance Act, 2002, w.e.f. 1-4-2003];
        (c) any sum received by an individual as a member of a Hindu undivided family, where such sum has been paid out of the income of the family, or, in the case where no such income has been paid to the family, the sum of the property of the family;
        (d) any sum received by a member of a co-operative society from such society as—
        """

    def add_documents(self, documents: List[Document]):
        """Add documents to the vector store."""
        if not self.collection or not self.embedding_model:
            logger.warning("Vector store/embedding model unavailable; skipping add_documents.")
            return

        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]

        embeddings = self.embedding_model.encode(texts).tolist()
        ids = [hashlib.md5((text + str(i)).encode()).hexdigest() for i, text in enumerate(texts)]

        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Added {len(documents)} documents to the vector store")

    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant documents based on query."""
        if not self.collection or not self.embedding_model:
            logger.info("Vector search unavailable; returning empty results")
            return []

        query_embedding = self.embedding_model.encode([query]).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            include=['documents', 'metadatas', 'distances']
        )

        formatted_results = []
        for i in range(len(results['ids'][0])):
            formatted_results.append({
                'id': results['ids'][0][i],
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i],
                'relevance_score': 1 - results['distances'][0][i]
            })

        return formatted_results

    def assess_risk(self, query: str) -> str:
        """Assess the risk level of a query."""
        high_risk_keywords = [
            'tax evasion', 'avoid tax', 'illegal', 'fraud', 'penalty', 'prosecution',
            'black money', 'undisclosed income', 'shell company', 'round tripping'
        ]

        medium_risk_keywords = [
            'capital gains', 'foreign income', 'crypto', 'cryptocurrency', 'derivatives',
            'futures', 'options', 'speculative business', 'huf', ' hindu undivided family',
            'clubbing of income', 'deemed income'
        ]

        query_lower = query.lower()

        if any(keyword in query_lower for keyword in high_risk_keywords):
            return "HIGH"
        elif any(keyword in query_lower for keyword in medium_risk_keywords):
            return "MEDIUM"
        else:
            return "LOW"

    def generate_response(self, query: str) -> Dict[str, Any]:
        """Generate a response to a tax query with citations and risk assessment."""
        # Assess risk
        risk_level = self.assess_risk(query)

        # Search for relevant documents
        search_results = self.search(query, n_results=3)

        # If no relevant results found, return a safe response
        if not search_results:
            return {
                "answer": "I couldn't find specific information about your query in the tax act. Please consult with a tax professional for personalized advice.",
                "sources": [],
                "risk_level": risk_level,
                "confidence": "LOW"
            }

        # Construct answer with citations
        answer_parts = []
        sources = []

        for i, result in enumerate(search_results):
            answer_parts.append(f"According to the Income Tax Act: {result['text'][:200]}...")
            sources.append({
                "id": result['id'],
                "text_preview": result['text'][:100] + "...",
                "metadata": result['metadata'],
                "relevance": result['relevance_score']
            })

        # Combine answer parts
        answer = " ".join(answer_parts)

        # Add disclaimer based on risk level
        disclaimer = ""
        if risk_level == "HIGH":
            disclaimer = "\n\n⚠️ HIGH RISK QUERY: This query involves areas that may have legal implications. Please consult with a qualified tax professional or chartered accountant before proceeding."
        elif risk_level == "MEDIUM":
            disclaimer = "\n\n⚠️ MEDIUM RISK QUERY: This query involves moderately complex tax matters. Consider consulting with a tax professional for personalized advice."

        answer += disclaimer

        return {
            "answer": answer,
            "sources": sources,
            "risk_level": risk_level,
            "confidence": "HIGH" if len(sources) > 0 and sources[0]['relevance'] > 0.7 else "MEDIUM"
        }

# Global RAG instance
tax_rag = TaxRAGSystem()