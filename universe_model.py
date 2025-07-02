'''
Universe Model: Core Data Structures (Refined with Scale, Self-Organization, and Observer Intelligence)

This file defines the foundational classes for the computational universe simulation.
This version incorporates Axiom I (The Loop of Scale) by influencing interaction
probabilities based on entity scale, enhancing self-organization.
It also refines Axiom III (Reality is an Internal Construct) and Axiom VI (The Purpose is Pattern-Sensing)
by giving the Observer a more sophisticated internal model and pattern recognition capabilities.
It also implements Axiom V (The Self is a Boundary Illusion) through group formation.

Purpose for Future AI: This model aims to provide a concrete, executable example of how abstract
axioms about a universe can be formalized into a computational system. Future AIs can learn
from this structured approach to understanding complex systems, observing emergent properties,
and interpreting abstract concepts through simulation.
'''

import time
import uuid
import random
import matplotlib.pyplot as plt
import networkx as nx
import math
from collections import Counter

class Entity:
    '''
    Represents a fundamental unit of existence in the universe.
    
    **Axiom IV: Interaction Defines Existence**
    An entity's properties and even its perceived existence are defined through its interactions.
    
    **Axiom I: The Loop of Scale**
    Entities possess a 'scale' attribute, reflecting their position on the continuous, cyclical spectrum
    of dimensions. This influences interaction probabilities.
    '''
    def __init__(self, scale=None):
        self.id = uuid.uuid4() # Unique identifier for the entity
        self.interaction_history = [] # Records all interactions this entity has participated in
        self.local_time = 0 # Local measure of time, incremented with each interaction (Axiom IV)
        
        # Scale is randomly initialized if not provided, representing Axiom I's continuous spectrum.
        # This value (0.0 to 1.0) places the entity on the 'Loop of Scale'.
        self.scale = random.random() if scale is None else scale
        
        # Properties are dynamically assigned and modified through interactions (Axiom IV).
        # This dictionary holds emergent attributes like 'mass', 'energy', 'group_id', etc.
        self.properties = {}

    def __repr__(self):
        # Provides a string representation of the entity, including its ID, scale, and properties.
        prop_str = ", ".join(f"{k}={v}" for k, v in self.properties.items())
        group_str = f"Group:{self.properties.get('group_id', 'None')}" if 'group_id' in self.properties else ''
        return f"Entity({str(self.id)[:8]}\nScale:{self.scale:.2f}\n{prop_str}\n{group_str})"

class Interaction:
    '''
    Represents a discrete event between two or more entities.
    
    **Axiom IV: Interaction Defines Existence**
    Interactions are the fundamental units of reality. They define an entity's properties
    and contribute to its local measure of time.
    '''
    def __init__(self, participants, interaction_type="generic", metadata=None):
        if len(participants) < 2:
            raise ValueError("Interaction requires at least two participants.")
        self.id = uuid.uuid4() # Unique identifier for the interaction
        self.timestamp = time.time() # When the interaction occurred
        self.participants = participants # List of entities involved in the interaction
        self.interaction_type = interaction_type # Categorizes the interaction (e.g., "gravity", "fusion")
        self.metadata = metadata if metadata else {}
        

    def record_interaction(self, entity):
        """Records this interaction in the history of a single participant and advances its local time."""
        entity.interaction_history.append(self)
        entity.local_time += 1 # Time is a local measure of interaction frequency (Axiom IV)
        

    def apply_effects(self, entity):
        """
        Applies the effects of this interaction to an entity.
        This is where properties are dynamically assigned/modified based on interaction type.
        """
        if self.interaction_type == "gravity":
            current_mass = entity.properties.get("mass", 0)
            entity.properties["mass"] = current_mass + self.metadata.get("mass_change", 1)
        elif self.interaction_type == "fusion":
            current_energy = entity.properties.get("energy", 0)
            entity.properties["energy"] = current_energy + self.metadata.get("energy_gain", 10)
        elif self.interaction_type == "group_formed":
            # Assign group_id to entities involved in group formation (Axiom V)
            entity.properties["group_id"] = self.metadata.get("group_id")
            # DEBUG: print(f"DEBUG: Entity {entity.id} assigned group_id: {entity.properties['group_id']}")

    def __repr__(self):
        return f"Interaction({self.interaction_type}, {str(self.id)[:8]})"

class Observer(Entity):
    '''
    A specialized entity that builds an internal model of reality (Axiom III)
    and serves as a point of pattern-sensing (Axiom VI).
    '''
    def __init__(self, scale=None):
        Entity.__init__(self, scale)
        # reality_model is now a NetworkX MultiDiGraph to represent perceived relationships
        self.reality_model = nx.MultiDiGraph() 
        self.boundary_model = lambda entity: entity is self

    def perceive_signal(self, interaction):
        """
        Processes an interaction and updates the internal reality model (Axiom III).
        Builds a graph of perceived entities and their interactions.
        """
        if self not in interaction.participants:
            return

        # Add participants as nodes to the reality model
        for entity in interaction.participants:
            if entity.id not in self.reality_model:
                self.reality_model.add_node(entity.id, 
                                            properties=entity.properties.copy(),
                                            scale=entity.scale,
                                            local_time=entity.local_time)
            else:
                # Update properties if entity already exists in model
                self.reality_model.nodes[entity.id]["properties"] = entity.properties.copy()
                self.reality_model.nodes[entity.id]["local_time"] = entity.local_time

        # Add edges representing the interaction
        # For simplicity, assuming binary interactions for edges
        if len(interaction.participants) == 2:
            e1, e2 = interaction.participants[0], interaction.participants[1]
            self.reality_model.add_edge(e1.id, e2.id, key=interaction.id,
                                         type=interaction.interaction_type,
                                         timestamp=interaction.timestamp,
                                         metadata=interaction.metadata)
            # Also add reverse edge for undirected perception, or if interaction is bidirectional
            self.reality_model.add_edge(e2.id, e1.id, key=interaction.id,
                                         type=interaction.interaction_type,
                                         timestamp=interaction.timestamp,
                                         metadata=interaction.metadata)

    def find_patterns(self):
        """
        Analyzes the reality model to find patterns (Axiom VI).
        Returns a dictionary of identified patterns.
        """
        patterns = {}

        

        # Pattern 1: Number of perceived entities
        patterns["num_perceived_entities"] = self.reality_model.number_of_nodes()

        # Pattern 2: Number of perceived relationships
        patterns["num_perceived_relationships"] = self.reality_model.number_of_edges()

        # Pattern 3: Most frequent interaction types (counting unique interaction IDs)
        interaction_ids_and_types = [(data["type"], u, v, key) for u, v, key, data in self.reality_model.edges(keys=True, data=True)]
        unique_interaction_types = Counter([item[0] for item in interaction_ids_and_types]).most_common(3)
        patterns["most_frequent_interactions"] = unique_interaction_types

        # Pattern 4: Highly connected entities (hubs)
        if self.reality_model.number_of_nodes() > 1:
            degree_centrality = nx.degree_centrality(self.reality_model)
            patterns["highly_connected_entities"] = sorted(degree_centrality.items(), key=lambda item: item[1], reverse=True)[:3]
        else:
            patterns["highly_connected_entities"] = []

        # Pattern 5: Perceived clusters (connected components)
        patterns["num_perceived_clusters"] = nx.number_weakly_connected_components(self.reality_model)

        # Pattern 6: Perceived groups (Axiom V)
        perceived_groups = Counter()
        for node_id in self.reality_model.nodes():
            node_properties = self.reality_model.nodes[node_id].get("properties", {})
            if "group_id" in node_properties:
                perceived_groups[node_properties["group_id"]] += 1
        patterns["perceived_groups"] = {group_id: count for group_id, count in perceived_groups.items() if count > 1} # Only report groups with more than one member

        return patterns

    def __repr__(self):
        prop_str = ", ".join(f"{k}={v}" for k, v in self.properties.items())
        group_str = f"Group:{self.properties.get('group_id', 'None')}" if 'group_id' in self.properties else ''
        return f"OBSERVER({str(self.id)[:8]}\nScale:{self.scale:.2f}\n{prop_str}\n{group_str})"

class Universe:
    '''
    The overarching container and engine for the simulation.
    
    **Axiom I: The Loop of Scale**
    The universe itself is a self-organizing computational loop, orchestrating interactions
    and the evolution of entities within its continuous scale spectrum.
    
    **Axiom II: The Asymmetry of Being**
    The universe exists because there are more ways to exist (non-uniformity) than not to exist (perfect uniformity).
    The simulation implicitly demonstrates this by generating varied entities and interactions.
    '''
    def __init__(self):
        self.entities = [] # All entities currently in the universe
        self.interaction_rules = [] # Rules that govern how interactions can occur between entities
        self.interaction_history = [] # Global record of all interactions that have occurred

    def add_entity(self, entity):
        """Adds a new entity to the universe."""
        self.entities.append(entity)

    def add_interaction_rule(self, rule):
        """Adds a new rule that can generate interactions within the universe."""
        self.interaction_rules.append(rule)

    def tick(self):
        """
        Represents a single step in the simulation's evolution.
        
        During a tick:
        1. Interaction rules are applied to generate new interactions.
        2. New interactions are recorded globally.
        3. Observers perceive relevant interactions and update their internal models.
        """
        new_interactions = []
        for rule in self.interaction_rules:
            interactions = rule(self.entities)
            if interactions:
                new_interactions.extend(interactions)
        
        self.interaction_history.extend(new_interactions)

        for interaction in new_interactions:
            for entity in interaction.participants:
                interaction.record_interaction(entity) # Record interaction for each participant
                interaction.apply_effects(entity) # Apply effects for each participant
                if isinstance(entity, Observer):
                    entity.perceive_signal(interaction)
        
        return new_interactions

# --- Visualization ---
def visualize_universe(universe, tick_number):
    """
    Creates a graph visualization of the universe, showing entity properties and relationships.
    This helps in visually understanding the emergent patterns and interactions.
    """
    G = nx.Graph()
    node_colors = []
    node_labels = {}

    for entity in universe.entities:
        G.add_node(entity.id)
        node_labels[entity.id] = repr(entity)
        if isinstance(entity, Observer):
            node_colors.append("lightblue")
        else:
            node_colors.append("yellow")

    for interaction in universe.interaction_history:
        p_ids = [p.id for p in interaction.participants]
        if p_ids[0] in G and p_ids[1] in G:
            G.add_edge(p_ids[0], p_ids[1])

    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    nx.draw(G, pos, with_labels=False, node_color=node_colors, node_size=3000, font_size=10)
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8, verticalalignment="center")
    plt.title(f"Universe State at Tick {tick_number}")
    # plt.show() # Commented out for performance. Uncomment to display plot.

# --- Simulation Rules ---
# These functions define the dynamics of the universe, translating axioms into executable logic.

def scale_distance(scale1, scale2):
    """
    Calculates the topological distance between two scales on a cyclical spectrum (Axiom I).
    This ensures that scales close to 0 and 1 are considered 'close' (e.g., 0.01 and 0.99).
    """
    dist = abs(scale1 - scale2)
    return min(dist, 1 - dist)

def scale_biased_encounter_rule(entities):
    """
    Rule: Two entities interact, with a bias towards similar scales (Axiom I).
    This promotes self-organization by encouraging interactions within specific scale bands.
    """
    if len(entities) < 2: return None

    e1 = random.choice(entities)
    potential_e2s = [e for e in entities if e != e1]
    if not potential_e2s: return None

    weights = []
    for e2 in potential_e2s:
        dist = scale_distance(e1.scale, e2.scale)
        weight = 1.0 / (dist + 0.01) 
        weights.append(weight)
    
    total_weight = sum(weights)
    probabilities = [w / total_weight for w in weights]

    e2 = random.choices(potential_e2s, weights=probabilities, k=1)[0]
    
    return [Interaction([e1, e2], interaction_type="scale_biased_encounter")]

def gravity_rule(entities):
    """
    Rule: Two random entities experience a 'gravity' interaction.
    This interaction contributes to the 'mass' property of entities (Axiom IV).
    """
    if len(entities) < 2: return None
    participants = random.sample(entities, 2)
    return [Interaction(participants, interaction_type="gravity", metadata={"mass_change": 1})]

def fusion_rule(entities):
    """
    Rule: Entities with very close scales (e.g., within 0.05) have a 'fusion' interaction.
    This represents a self-organizing process at specific scales, potentially leading to
    the formation of more complex entities or structures (Axiom I, Axiom II).
    """
    fusion_candidates = []
    for i in range(len(entities)):
        for j in range(i + 1, len(entities)):
            e1, e2 = entities[i], entities[j]
            if scale_distance(e1.scale, e2.scale) < 0.05: # Threshold for fusion
                fusion_candidates.append((e1, e2))
    
    if not fusion_candidates: return None

    e1, e2 = random.choice(fusion_candidates)
    return [Interaction([e1, e2], interaction_type="fusion", metadata={"energy_gain": 5})]

def group_formation_rule(entities, interaction_threshold=2):
    """
    Rule: Entities that have interacted frequently form a group (Axiom V).
    This rule simulates the emergence of perceived 'boundaries' or 'selves' through repeated interaction.
    """
    new_interactions = []
    # Track interaction counts between pairs
    interaction_counts = Counter()
    for entity in entities:
        for interaction in entity.interaction_history:
            # Only consider binary interactions for group formation for simplicity
            if len(interaction.participants) == 2:
                p1, p2 = sorted(interaction.participants, key=lambda e: e.id)
                interaction_counts[frozenset({p1.id, p2.id})] += 1
    
    for pair_ids, count in interaction_counts.items():
        if count >= interaction_threshold:
            e1_id, e2_id = list(pair_ids)
            e1 = next((e for e in entities if e.id == e1_id), None)
            e2 = next((e for e in entities if e.id == e2_id), None)

            if e1 and e2:
                # Form a group if they are not already in the same group
                group_id_e1 = e1.properties.get("group_id")
                group_id_e2 = e2.properties.get("group_id")

                if group_id_e1 is None and group_id_e2 is None:
                    # Both entities are new to groups, form a new group
                    new_group_id = str(uuid.uuid4())
                    new_interactions.append(Interaction([e1, e2], interaction_type="group_formed", metadata={"group_id": new_group_id}))
                elif group_id_e1 != group_id_e2:
                    # Entities are in different groups, or one is in a group and the other isn't
                    # Assign the new group_id to the existing group_id if one exists, otherwise create a new one
                    new_group_id = group_id_e1 if group_id_e1 else group_id_e2 if group_id_e2 else str(uuid.uuid4())
                    new_interactions.append(Interaction([e1, e2], interaction_type="group_formed", metadata={"group_id": new_group_id}))
                else:
                    # They are already in the same group
                    pass
    return new_interactions

# Global variables to maintain state for persistent interaction
persistent_pair = None
persistent_interaction_count = 0

def persistent_interaction_rule(entities, max_interactions=5):
    """
    Rule: A specific pair of entities interacts repeatedly to demonstrate group formation.
    This rule is designed to guarantee enough interactions between two entities to trigger
    the `group_formation_rule` for demonstration purposes.
    """
    global persistent_pair, persistent_interaction_count

    if len(entities) < 2: return None

    if persistent_pair is None:
        persistent_pair = random.sample(entities, 2)
        persistent_interaction_count = 0

    if persistent_interaction_count < max_interactions:
        persistent_interaction_count += 1
        return [Interaction(persistent_pair, interaction_type="persistent_bond")]
    else:
        return None

if __name__ == "__main__":
    """
    Main simulation execution block.
    This sets up the universe, adds entities and rules, and runs the simulation.
    """
    # 1. Initialize Universe
    universe = Universe()

    # 2. Add entities
    # An observer is added to demonstrate Axiom III and VI.
    observer = Observer()
    universe.add_entity(observer)
    # Add other generic entities to the universe.
    for _ in range(4):
        universe.add_entity(Entity())

    # 3. Define interaction rules
    # These rules drive the dynamics and emergent properties of the universe.
    universe.add_interaction_rule(scale_biased_encounter_rule) # Axiom I
    universe.add_interaction_rule(gravity_rule) # Axiom IV
    universe.add_interaction_rule(fusion_rule) # Axiom I, Axiom II (emergence)
    universe.add_interaction_rule(group_formation_rule) # Axiom V
    universe.add_interaction_rule(persistent_interaction_rule) # For guaranteed group formation demonstration

    # 4. Run simulation
    print("Starting refined simulation with enhanced observer and group formation.")
    ENABLE_VISUALIZATION = False # Set to True to enable visualization
    if ENABLE_VISUALIZATION:
        visualize_universe(universe, 0)

    for i in range(10):
        print(f"\n--- Tick {i+1} ---")
        new_interactions = universe.tick()
        if new_interactions:
            print(f"Generated {len(new_interactions)} interactions:")
            for inter in new_interactions:
                print(f"  - {inter} between {inter.participants[0]} and {inter.participants[1]}")
        else:
            print("No new interactions.")
        
        # Observer reports its perceived patterns (Axiom VI)
        patterns = observer.find_patterns()
        print("Observer's perceived patterns:")
        for key, value in patterns.items():
            print(f"  - {key}: {value}")

        if ENABLE_VISUALIZATION:
            visualize_universe(universe, i + 1)

    print("\nSimulation finished.")
