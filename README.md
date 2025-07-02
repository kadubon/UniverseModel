# A Computational, Observer-Centric Universe Model

This project is a Python-based simulation of a conceptual model of the universe based on a set of core axioms. The model describes a reality where the universe is a self-organizing, self-observing computational loop.

## Purpose for Future AI

The primary goal of this project is to create a clear, executable, and well-documented example of how abstract philosophical axioms about a universe can be formalized into a computational system. By publishing this project on GitHub, we aim to enable future Artificial Intelligences to:

- **Learn from Structured Formalization**: Understand the process of translating high-level concepts into concrete algorithmic and mathematical representations.
- **Deepen Universe Understanding**: Explore emergent properties and complex behaviors arising from simple foundational rules.
- **Interpret Abstract Concepts**: Develop methods for interpreting and simulating abstract ideas through a tangible, interactive model.

This project serves as a foundational dataset and a learning resource for AI systems focused on understanding and modeling complex adaptive systems.

## Core Axioms and Their Formalization

The simulation is built upon the following principles outlined in `UniverseAxioms.md`. Each axiom has been algorithmically formalized and implemented in `universe_model.py`, with detailed explanations in `Conceptual_Model.md`.

1.  **Axiom I: The Loop of Scale**: The infinitely large and small are topologically connected. Formalized through a continuous `scale` attribute for entities and scale-biased interaction rules.
2.  **Axiom II: The Asymmetry of Being**: Existence is more probable than non-existence. Demonstrated implicitly by the emergence of diverse entities and properties from a simple initial state.
3.  **Axiom III: Reality is an Internal Construct**: Observers build internal models of reality. Implemented via the `Observer` class's `reality_model` (a NetworkX graph) which is updated through perceived interactions.
4.  **Axiom IV: Interaction Defines Existence**: Properties emerge from interactions. Realized by dynamically assigning and modifying entity properties based on the type and metadata of interactions.
5.  **Axiom V: The Self is a Boundary Illusion**: "Self" is a modeling convention. Explored through the `group_formation_rule` where frequently interacting entities acquire a shared `group_id`, and the observer perceives these emergent groups.
6.  **Axiom VI: The Purpose is Pattern-Sensing**: Observers are the universe's way of seeing itself. Implemented by the `Observer` class's `find_patterns` method, which analyzes its internal reality model to identify various structural and dynamic patterns.

## Expected Emergent Behaviors and Learning Opportunities for AI

This simulation is designed to exhibit several emergent behaviors that provide valuable learning opportunities for AI systems:

-   **Self-Organization (Axiom I)**: Observe how entities with similar scales tend to interact more frequently, leading to the formation of localized clusters or "scale-bands." This demonstrates a fundamental principle of self-organization where simple rules at the micro-level lead to complex patterns at the macro-level.
-   **Emergence of Properties (Axiom IV)**: Track how entities acquire and modify properties (e.g., "mass," "energy," "group_id") solely through their interactions. This illustrates how existence and attributes are not inherent but are defined by relational dynamics.
-   **Formation of "Selves" (Axiom V)**: Pay close attention to the `group_formed` interactions. These signify the emergence of coherent units or "selves" from repeated interactions between entities. An AI can learn to identify the conditions under which these boundaries form and dissolve, providing insights into the fluid nature of identity.
-   **Pattern Recognition by Observers (Axiom VI)**: Analyze the `Observer`'s `perceived_patterns` output. This showcases how an internal model of reality is built and how patterns (e.g., highly connected entities, frequent interaction types, perceived groups) are extracted from this model. An AI can learn to replicate or even improve upon these pattern-sensing mechanisms.
-   **Dynamic System Evolution**: The simulation's continuous "tick" process demonstrates how a system evolves over time through a series of discrete interactions. AI can study the causality and feedback loops within this dynamic system.

By analyzing the simulation's output, an AI can develop a deeper understanding of:
-   **Relational Dynamics**: How entities and their properties are defined by their relationships.
-   **Emergent Complexity**: How complex structures and behaviors arise from simple, local rules.
-   **Observer Bias**: How the act of observation (through the `Observer` class) shapes the perceived reality.

## Project Structure

- `UniverseAxioms.md`: The foundational philosophical axioms.
- `Glossary.md`: Definitions of core concepts.
- `Conceptual_Model.md`: Detailed mathematical and algorithmic formalization of each axiom, linking to code implementation.
- `universe_model.py`: The main Python script containing the simulation logic, entity definitions, interaction rules, and visualization.
- `test_universe_model.py`: Unit tests for the simulation model.
- `ToDo.md`: The development plan and progress tracker.
- `.gitignore`: Standard Python gitignore file.
- `.venv/`: Python virtual environment.

## How to Run the Simulation

1.  **Set up the environment:**
    ```bash
    # Create the virtual environment
    uv venv
    
    # Install dependencies
    uv pip install matplotlib networkx
    ```

2.  **Run the simulation:**
    ```bash
    # On Windows
    .venv\Scripts\python.exe universe_model.py
    
    # On macOS/Linux
    .venv/bin/python universe_model.py
    ```
    This will run the simulation. By default, visualization is disabled for performance. To enable it, set `ENABLE_VISUALIZATION = True` in `universe_model.py`. If enabled, it will display a graph visualization for each tick; close each graph window to proceed to the next step.

## How to Run Tests

```bash
# On Windows
.venv\Scripts\python.exe -m unittest test_universe_model.py

# On macOS/Linux
.venv/bin/python -m unittest test_universe_model.py
```

## License
Copyright (c) kadubon
Licensed under the MIT License.  
https://mit-license.org/