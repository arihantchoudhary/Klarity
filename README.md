# Project Klarity

Welcome to Project Klarity, a monorepo dedicated to advanced document processing and AI-driven solutions. This repository is used as a work trial sandbox where all experiments, proofs-of-concept, and production-oriented skeletons are developed and refined. Below is an overview of the repository structure, the current inner workings of each folder, and the status of our work trial.

---

## Repository Structure & Inner Workings

### ask-ai-framework
**Purpose:** This is the core development hub where interactive notebooks drive rapid experimentation and iterative improvements.
- **Interactive Notebooks:** These notebooks cover document ingestion, preprocessing, transformation, analysis, and evaluation processes. They are the primary space where end-to-end workflows are prototyped.
- **Modular Experimentation:** Individual stages – such as file processing, content extraction, and downstream analytics – are developed and tested here in modular fashion.
- **Current Status:** The skeleton design is set up, and notebooks are gradually being populated with functional pipelines. At this stage, work is focused on outlining workflows and validating proof-of-concept modules.

### indexing_millions
**Purpose:** Implements strategies for lightning-fast indexing of document data.
- **Inference Optimization:** Techniques are explored to utilize GPU resources minimally while processing large volumes of documents quickly.
- **Algorithm Experiments:** Contains scripts and experiments for various indexing algorithms and data structures aimed at improving retrieval speeds.
- **Current Status:** Experimental scripts and prototype notebooks are in place, testing different approaches to achieve optimal indexing performance.

### mistral-ocr
**Purpose:** Dedicated to experimenting with the Mistral OCR API.
- **API Integrations:** Implements interactions with the Mistral OCR API to extract structured text and images from documents (images, PDFs).
- **Batch Processing:** Work is underway to support single and batch processing modes.
- **Current Status:** Functional prototypes are available that use the Mistral API for document understanding. The focus here is on refining the OCR results and extending batch capabilities.

### ask-ai-production-skeleton
**Purpose:** Provides a skeletal codebase intended for future production deployment of the Ask AI project.
- **Production Blueprint:** Acts as the envisioned final architecture. It is under continuous review (e.g., by Arun) to ensure it meets high production standards.
- **Integration Testing:** Will eventually consolidate the proven modules from the ask-ai-framework into a cohesive production system.
- **Current Status:** Still in a skeletal phase with placeholder modules; integration efforts are planned as more components in ask-ai-framework become production-ready.

### Go_JS react libraries
**Purpose:** Houses resources for dynamic diagram generation and interactive visualizations.
- **UX & Visualizations:** Provides React components, templates, and assets for generating flowcharts, design patterns, and interactive visual representations of processes.
- **Current Status:** Contains foundational components that serve as a resource hub. Work here focuses on creating engaging visualizations that can be integrated into the overall project dashboards.

---

## Project Status & Work Trial

This repository is dedicated to my work trial efforts. It serves as a comprehensive sandbox where every experiment, proof-of-concept, and production-oriented module is developed and iterated upon. The emphasis is on rapid prototyping using interactive notebooks (especially within **ask-ai-framework**) to simulate complete workflows before they are transitioned into a production-grade environment.

Key points:
- **Rapid Experimentation:** The ask-ai-framework is the primary environment for developing and testing end-to-end document processing pipelines.
- **Iterative Integration:** Individual successes in indexing, OCR, and process modularity will later be merged into the production skeleton.
- **Work Trial Focus:** The repository reflects ongoing innovation and continuous improvement, making it an ideal showcase of progressive work trial outputs.

---

## Getting Started

1. **Explore the Notebooks:** Begin with the interactive notebooks in **ask-ai-framework** to review the current experimental workflows.
2. **Review Each Module:** Look into the specific directories (indexing_millions, mistral-ocr, ask-ai-production-skeleton, Go_JS react libraries) for detailed insights into how each component is being developed.
3. **Follow the Roadmap:** Check out the deployment files and technical documentation for insight into future integration plans and system scalability.

---

## Contributing

Contributions are welcome. Please refer to the CONTRIBUTING.md file for guidelines on how to contribute, report issues, and propose enhancements. Your input is valuable for refining the integration and production-readiness of the project during this work trial phase.

---

## License

This project is licensed under the [Your License Name] License.
