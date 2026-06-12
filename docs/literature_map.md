        # Literature Map

        Paper: 118 world_model_audits_from_failed_rollouts

        Field box: robot world-model evaluation

        Thesis: World-Model Audits From Failed Rollouts turns the seed bet into a mechanism: Use failed rollouts to localize which physical assumptions the world model lacks.

        ## Landscape Sweep Summary
        The selector ranked records from the shared 500,000-record pool. The closest visible clusters are:
        - LLM-Based Control for Simulated Physical Reasoning: Modular Evaluation in the NeurIPS Embodied Agent Interface Challenge (2026)
- WorldGym: World Model as An Environment for Policy Evaluation (2025)
- A Gaussian Process State Space Model Fusion Physical Model and Residual Analysis for Fatigue Evaluation (2022)
- Lead Me by the Hand: Evaluation of a Direct Physical Interface for Nursing Assistant Robots (2010)
- Real-World Evaluation of Regulatory Judgments on Anticancer Drug Use During Pregnancy in Japan: A Retrospective Analysis from 2004 to 2024 (2025)
- Fatigue life evaluation of root failure in welded joints based on displacement around the weld root (2025)
- Evaluation of the use of Robotics in Hotels in terms of Customer Satisfaction (2023)
- Lead me by the hand: Evaluation of a direct physical interface for nursing assistant robots (2010)
- "Global Action Plan on Physical Activity 2018–2030: More Active People For A Healthier World" (2024)
- Digital Twin-Driven Virtual Control Technology of Home-Use Robot: Human-Cyber-Physical System (2022)
- From Cyber–Physical Convergence to Digital Twins: A Review on Edge Computing Use Case Designs (2023)
- WorldBench: Disambiguating Physics for Diagnostic Evaluation of World Models (2026)

        ## Hidden Assumptions
        - The executed trajectory is a sufficient training target.
- Unobserved physical alternatives can be averaged into uncertainty.
- Task labels capture the mechanism that caused failure.
- A planner only needs nominal feasibility.
- Embodiment-specific contact effects are nuisance variation.

        ## Boundary
        The project avoids weak moves such as bigger models, generic uncertainty, or a benchmark-only contribution. It centers a mechanism-level change: World model audits from failed rollouts keeps action-critical alternatives explicit until a physical observation collapses them.
