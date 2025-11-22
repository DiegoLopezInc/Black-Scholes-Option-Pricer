"""
Mathematical Concept Search Interface

searchthearXiv-style interface for querying mathematical concepts,
optimization techniques, and Greek symbols with NLP-powered search.

Inspired by: https://www.searchthearxiv.com/
"""

import streamlit as st
import sys
import os
from typing import List, Dict
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.knowledge.math_concepts import (
    MATHEMATICAL_GREEKS,
    OPTIONS_GREEKS,
    OPTIMIZATION_TECHNIQUES,
    MATHEMATICAL_CONCEPTS,
    search_concepts,
    get_related_concepts,
    export_to_sonnet_prompt
)

# Check for Together AI
try:
    from together import Together
    TINKER_KEY = os.environ.get('TINKER_KEY', '')
    HAS_TINKER = bool(TINKER_KEY)
except ImportError:
    HAS_TINKER = False

st.set_page_config(
    page_title="Mathematical Concept Search",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .concept-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #4CAF50;
    }
    .greek-symbol {
        font-size: 3em;
        font-weight: bold;
        color: #2196F3;
    }
    .formula {
        font-family: 'Courier New', monospace;
        background-color: #fff3cd;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .export-button {
        background-color: #8B5CF6;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'query_success_rate' not in st.session_state:
    st.session_state.query_success_rate = []
if 'export_mode' not in st.session_state:
    st.session_state.export_mode = False

st.title("🔍 Mathematical Concept Search")
st.markdown("*Search mathematical concepts, Greeks, optimization techniques, and research connections*")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    search_mode = st.radio(
        "Search Mode",
        ["Quick Search", "NLP-Powered Search", "Browse Categories", "Query Analytics"]
    )

    st.markdown("---")
    st.markdown("### References")
    st.markdown("[Terence Tao's Blog](https://terrytao.wordpress.com/)")
    st.markdown("[AlphaEvolve Repository](https://github.com/google-deepmind/alphaevolve_repository_of_problems)")
    st.markdown("[arXiv.org](https://arxiv.org/)")

    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This tool helps you discover mathematical concepts and their connections.

    **Features:**
    - Search 20+ Greek symbols
    - 8 financial Greeks
    - Optimization techniques
    - Terence Tao's research
    - Export to Sonnet 4.5
    """)

if search_mode == "Quick Search":
    st.header("Quick Concept Search")

    # Search box
    query = st.text_input(
        "Search for mathematical concepts, Greeks, or optimization techniques",
        placeholder="e.g., variance reduction, delta, gradient descent, zeta function"
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        search_button = st.button("🔍 Search", type="primary")
    with col2:
        max_results = st.number_input("Max results", 1, 50, 10)

    if search_button and query:
        # Track query
        st.session_state.search_history.append(query)

        results = search_concepts(query, max_results)

        if results:
            st.success(f"Found {len(results)} results for '{query}'")

            # Record success
            st.session_state.query_success_rate.append(1)

            # Display results
            for idx, result in enumerate(results):
                with st.expander(f"📚 {result.get('type', 'unknown').replace('_', ' ').title()}: {result.get('name', result.get('category', 'Unknown'))}"):
                    result_type = result['type']

                    if result_type == 'mathematical_greek':
                        details = result['details']
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            st.markdown(f"<div class='greek-symbol'>{details['symbol']}</div>", unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"**Symbol:** {details['symbol']}")
                            st.markdown(f"**Fields:** {', '.join(details['fields'])}")
                            st.markdown("**Uses:**")
                            for use in details['uses']:
                                st.markdown(f"- {use}")
                            if 'related_to' in details:
                                st.markdown(f"**Related concepts:** {', '.join(details['related_to'])}")

                    elif result_type == 'options_greek':
                        details = result['details']
                        st.markdown(f"### {details['symbol']} - {result['name'].title()}")
                        st.markdown(f"<div class='formula'>{details['formula']}</div>", unsafe_allow_html=True)
                        st.markdown(f"**Meaning:** {details['meaning']}")
                        if 'interpretation' in details:
                            st.markdown(f"**Interpretation:** {details['interpretation']}")
                        if 'range_call' in details:
                            st.markdown(f"**Call range:** {details['range_call']}")
                        if 'range_put' in details:
                            st.markdown(f"**Put range:** {details['range_put']}")

                    elif result_type == 'optimization':
                        details = result['details']
                        st.markdown(f"**Category:** {details.get('category', 'Unknown')}")
                        if 'techniques' in details:
                            for tech_name, tech_details in details['techniques'].items():
                                st.markdown(f"**{tech_name.replace('_', ' ').title()}**")
                                st.markdown(f"- {tech_details.get('description', 'No description')}")
                                if 'variance_reduction' in tech_details:
                                    st.markdown(f"- Variance Reduction: {tech_details['variance_reduction']}")
                                if 'reference' in tech_details:
                                    st.markdown(f"- Reference: {tech_details['reference']}")

                    elif result_type == 'concept':
                        details = result['details']
                        st.json(details)

                    # Export button
                    export_data = {
                        'name': result.get('name', result.get('category', 'Unknown')),
                        'type': result_type,
                        'details': result.get('details', {})
                    }

                    if st.button(f"📤 Export to Sonnet 4.5 Prompt", key=f"export_{idx}"):
                        markdown_prompt = export_to_sonnet_prompt(export_data)
                        st.markdown("### Copy this prompt to Claude Sonnet 4.5:")
                        st.code(markdown_prompt, language='markdown')
                        st.markdown("*Prompt copied! Paste it into Claude to continue your research.*")

        else:
            st.warning(f"No results found for '{query}'. Try different keywords.")
            st.session_state.query_success_rate.append(0)

            # Suggestions
            st.info("💡 **Suggestions:**")
            st.markdown("- Try: *delta*, *variance*, *convergence*, *gradient*")
            st.markdown("- Search for Greek letters: *alpha*, *beta*, *gamma*")
            st.markdown("- Look for techniques: *monte carlo*, *optimization*")

elif search_mode == "NLP-Powered Search":
    st.header("🤖 NLP-Powered Semantic Search")

    if not HAS_TINKER:
        st.warning("⚠️ TINKER_KEY not found in environment. NLP search requires Together AI API.")
        st.markdown("Set `TINKER_KEY` to enable AI-powered search.")
    else:
        st.success("✅ Together AI connected - NLP search enabled")

        natural_query = st.text_area(
            "Describe what you're looking for in natural language",
            placeholder="I'm trying to optimize a Monte Carlo simulation that's converging too slowly. What variance reduction techniques can I use?",
            height=100
        )

        if st.button("🔍 AI Search", type="primary"):
            if natural_query:
                with st.spinner("Analyzing query with AI..."):
                    try:
                        client = Together(api_key=TINKER_KEY)

                        # Use AI to extract concepts
                        prompt = f"""Given this mathematical/computational query, extract relevant search keywords:

Query: {natural_query}

Return a JSON array of 3-5 relevant keywords/concepts that would help search a mathematical knowledge base.
Focus on: mathematical concepts, Greek symbols, optimization techniques, statistical methods.

Respond with only the JSON array, no explanation."""

                        response = client.chat.completions.create(
                            model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                            messages=[{"role": "user", "content": prompt}],
                            max_tokens=100,
                            temperature=0.3
                        )

                        keywords_text = response.choices[0].message.content.strip()

                        # Parse keywords
                        try:
                            if keywords_text.startswith('['):
                                keywords = json.loads(keywords_text)
                            else:
                                # Fallback: split by common separators
                                keywords = [k.strip() for k in keywords_text.split(',')]

                            st.info(f"🔑 Extracted keywords: {', '.join(keywords)}")

                            # Search for each keyword
                            all_results = []
                            for keyword in keywords:
                                results = search_concepts(keyword, 5)
                                all_results.extend(results)

                            # Deduplicate
                            seen = set()
                            unique_results = []
                            for result in all_results:
                                key = f"{result.get('type')}_{result.get('name', result.get('category'))}"
                                if key not in seen:
                                    seen.add(key)
                                    unique_results.append(result)

                            if unique_results:
                                st.success(f"Found {len(unique_results)} relevant concepts")

                                for idx, result in enumerate(unique_results[:10]):
                                    with st.expander(f"📚 {result.get('name', result.get('category', 'Unknown'))}"):
                                        st.json(result['details'])

                                        # Export button
                                        if st.button(f"📤 Export", key=f"nlp_export_{idx}"):
                                            export_data = {
                                                'name': result.get('name', result.get('category', 'Unknown')),
                                                'type': result['type'],
                                                'details': result.get('details', {}),
                                                'original_query': natural_query
                                            }
                                            markdown_prompt = export_to_sonnet_prompt(export_data)
                                            markdown_prompt += f"\n\n## Original Query\n\n{natural_query}\n"
                                            st.code(markdown_prompt, language='markdown')
                            else:
                                st.warning("No results found. Try rephrasing your query.")

                        except json.JSONDecodeError:
                            st.error("Could not parse AI response. Try a different query.")

                    except Exception as e:
                        st.error(f"AI search error: {e}")

elif search_mode == "Browse Categories":
    st.header("📖 Browse by Category")

    category = st.selectbox(
        "Select category",
        ["Mathematical Greeks", "Options Greeks", "Optimization Techniques", "Mathematical Concepts"]
    )

    if category == "Mathematical Greeks":
        st.subheader("Mathematical Greek Symbols")
        st.markdown("*Greek letters commonly used in mathematics and science*")

        for name, details in MATHEMATICAL_GREEKS.items():
            with st.expander(f"{details['symbol']} ({name})"):
                st.markdown(f"**Symbol:** {details['symbol']}")
                st.markdown(f"**Fields:** {', '.join(details['fields'])}")
                st.markdown("**Common uses:**")
                for use in details['uses']:
                    st.markdown(f"- {use}")

    elif category == "Options Greeks":
        st.subheader("Options Trading Greeks")
        st.markdown("*Risk sensitivities for options pricing*")

        cols = st.columns(2)
        for idx, (name, details) in enumerate(OPTIONS_GREEKS.items()):
            with cols[idx % 2]:
                st.markdown(f"### {details['symbol']} - {name.title()}")
                st.markdown(f"**Formula:** `{details['formula']}`")
                st.markdown(f"**Meaning:** {details['meaning']}")
                if 'interpretation' in details:
                    st.markdown(f"*{details['interpretation']}*")
                st.markdown("---")

    elif category == "Optimization Techniques":
        st.subheader("Optimization & Variance Reduction")

        for cat_name, cat_details in OPTIMIZATION_TECHNIQUES.items():
            st.markdown(f"## {cat_name.replace('_', ' ').title()}")
            st.markdown(f"**Category:** {cat_details.get('category', 'Unknown')}")

            if 'techniques' in cat_details:
                for tech_name, tech_details in cat_details['techniques'].items():
                    with st.expander(f"{tech_name.replace('_', ' ').title()}"):
                        for key, value in tech_details.items():
                            if isinstance(value, list):
                                st.markdown(f"**{key.replace('_', ' ').title()}:**")
                                for item in value:
                                    st.markdown(f"- {item}")
                            else:
                                st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")

            elif 'description' in cat_details:
                st.markdown(f"**Description:** {cat_details['description']}")
                if 'github' in cat_details:
                    st.markdown(f"[GitHub Repository]({cat_details['github']})")
                if 'paper' in cat_details:
                    st.markdown(f"**Paper:** {cat_details['paper']}")
                if 'authors' in cat_details:
                    st.markdown(f"**Authors:** {', '.join(cat_details['authors'])}")

elif search_mode == "Query Analytics":
    st.header("📊 Query Analytics & Fine-Tuning")

    if st.session_state.search_history:
        st.subheader("Search History")

        # Success rate
        if st.session_state.query_success_rate:
            success_rate = sum(st.session_state.query_success_rate) / len(st.session_state.query_success_rate)
            st.metric("Query Success Rate", f"{success_rate*100:.1f}%")

        # Recent searches
        st.markdown("**Recent Searches:**")
        for idx, query in enumerate(reversed(st.session_state.search_history[-10:])):
            st.markdown(f"{idx+1}. {query}")

        # Most common terms
        from collections import Counter
        all_words = []
        for query in st.session_state.search_history:
            all_words.extend(query.lower().split())

        word_counts = Counter(all_words)
        st.markdown("**Most searched terms:**")
        for word, count in word_counts.most_common(10):
            st.markdown(f"- **{word}**: {count} times")

        # Clear history
        if st.button("Clear History"):
            st.session_state.search_history = []
            st.session_state.query_success_rate = []
            st.rerun()

    else:
        st.info("No search history yet. Try searching for concepts!")

# Footer
st.markdown("---")
st.markdown("""
**Data Sources:**
- [Terence Tao - Mathematical exploration and discovery at scale](https://terrytao.wordpress.com/)
- [AlphaEvolve Repository](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
- [Variance Reduction Wikipedia](https://en.wikipedia.org/wiki/Variance_reduction)
- [Antithetic Variates](https://en.wikipedia.org/wiki/Antithetic_variates)

*Built with Streamlit | Powered by Together AI*
""")
