import unittest
import uuid
from collections import Counter
import networkx as nx
from universe_model import Entity, Interaction, Observer, Universe, scale_distance, scale_biased_encounter_rule, gravity_rule, fusion_rule, group_formation_rule, persistent_interaction_rule
import universe_model # Import the module to access global variables

class TestEntity(unittest.TestCase):
    def test_entity_creation(self):
        entity = Entity()
        self.assertIsInstance(entity.id, uuid.UUID)
        self.assertEqual(entity.interaction_history, [])
        self.assertEqual(entity.local_time, 0)
        self.assertIsInstance(entity.scale, float)
        self.assertGreaterEqual(entity.scale, 0.0)
        self.assertLessEqual(entity.scale, 1.0)
        self.assertEqual(entity.properties, {})

    def test_entity_repr_with_properties(self):
        entity = Entity(scale=0.5)
        entity.properties["mass"] = 10
        entity.properties["group_id"] = "abc"
        repr_str = repr(entity)
        self.assertIn("Entity(", repr_str)
        self.assertIn("Scale:0.50", repr_str)
        self.assertIn("mass=10", repr_str)
        self.assertIn("Group:abc", repr_str)

class TestInteraction(unittest.TestCase):
    def test_interaction_creation(self):
        entity1 = Entity()
        entity2 = Entity()
        interaction = Interaction([entity1, entity2], "test_interaction", metadata={"value": 100})
        self.assertEqual(len(interaction.participants), 2)
        self.assertEqual(interaction.interaction_type, "test_interaction")
        self.assertEqual(interaction.metadata["value"], 100)

    def test_interaction_records_history_and_applies_effects(self):
        entity1 = Entity()
        entity2 = Entity()
        # Test gravity effect
        interaction1 = Interaction([entity1, entity2], interaction_type="gravity", metadata={"mass_change": 2})
        interaction1.record_interaction(entity1)
        interaction1.apply_effects(entity1)
        interaction1.record_interaction(entity2)
        interaction1.apply_effects(entity2)
        self.assertEqual(len(entity1.interaction_history), 1)
        self.assertEqual(entity1.local_time, 1)
        self.assertEqual(entity1.properties["mass"], 2)
        self.assertEqual(entity2.properties["mass"], 2)

        # Test fusion effect
        interaction2 = Interaction([entity1, entity2], interaction_type="fusion", metadata={"energy_gain": 5})
        interaction2.record_interaction(entity1)
        interaction2.apply_effects(entity1)
        interaction2.record_interaction(entity2)
        interaction2.apply_effects(entity2)
        self.assertEqual(len(entity1.interaction_history), 2)
        self.assertEqual(entity1.local_time, 2)
        self.assertEqual(entity1.properties["energy"], 5)
        self.assertEqual(entity2.properties["energy"], 5)

        # Test group_formed effect
        test_group_id = str(uuid.uuid4())
        interaction3 = Interaction([entity1, entity2], interaction_type="group_formed", metadata={"group_id": test_group_id})
        interaction3.record_interaction(entity1)
        interaction3.apply_effects(entity1)
        interaction3.record_interaction(entity2)
        interaction3.apply_effects(entity2)
        self.assertEqual(entity1.properties["group_id"], test_group_id)
        self.assertEqual(entity2.properties["group_id"], test_group_id)

class TestNetworkX(unittest.TestCase):
    def test_networkx_multiple_edges(self):
        G = nx.MultiDiGraph()
        n1 = uuid.uuid4()
        n2 = uuid.uuid4()

        # Add first edge
        id1 = uuid.uuid4()
        G.add_edge(n1, n2, key=id1, type="A")
        G.add_edge(n2, n1, key=id1, type="A") # Reverse

        # Add second edge
        id2 = uuid.uuid4()
        G.add_edge(n1, n2, key=id2, type="A")
        G.add_edge(n2, n1, key=id2, type="A") # Reverse

        self.assertEqual(G.number_of_edges(), 4)

class TestObserver(unittest.TestCase):
    def test_observer_creation(self):
        observer = Observer()
        self.assertIsInstance(observer, Entity)
        self.assertIsInstance(observer.reality_model, nx.MultiDiGraph)

    def test_observer_perceives_signal(self):
        universe = Universe()
        observer = Observer()
        entity1 = Entity()
        universe.add_entity(observer)
        universe.add_entity(entity1)

        # Define a rule that makes observer and entity1 interact
        def specific_interaction_rule(entities):
            if observer in entities and entity1 in entities:
                return [Interaction([observer, entity1], interaction_type="test_perceive")]
            return []
        universe.add_interaction_rule(specific_interaction_rule)

        # Run a tick to make the interaction happen and be perceived
        new_interactions = universe.tick()
        self.assertEqual(len(new_interactions), 1)
        interaction = new_interactions[0] # Get the generated interaction
        
        self.assertIn(observer.id, observer.reality_model.nodes)
        self.assertIn(entity1.id, observer.reality_model.nodes)
        self.assertTrue(observer.reality_model.has_edge(observer.id, entity1.id, key=interaction.id))
        self.assertEqual(observer.reality_model.get_edge_data(observer.id, entity1.id, key=interaction.id)["type"], "test_perceive")

    def test_observer_finds_patterns(self):
        observer = Observer()
        e1 = Entity()
        e2 = Entity()
        e3 = Entity()

        # Set group_id properties before interactions are perceived
        e1.properties["group_id"] = "group1"
        e2.properties["group_id"] = "group1"
        e3.properties["group_id"] = "group2"
        e4 = Entity()
        e4.properties["group_id"] = "group2"

        # Manually create interactions and have the observer perceive them
        # This ensures precise control over what the observer sees.
        observer.perceive_signal(Interaction([observer, e1], interaction_type="type_A")) 
        observer.perceive_signal(Interaction([observer, e1], interaction_type="type_A")) 
        observer.perceive_signal(Interaction([observer, e2], interaction_type="type_B")) 
        observer.perceive_signal(Interaction([observer, e3], interaction_type="type_A")) 
        observer.perceive_signal(Interaction([observer, e4], interaction_type="type_B")) # Observer perceives e4
        observer.perceive_signal(Interaction([observer, e2], interaction_type="type_B")) 

        patterns = observer.find_patterns()

        self.assertEqual(patterns["num_perceived_entities"], 5) # observer, e1, e2, e3, e4
        self.assertEqual(patterns["num_perceived_relationships"], 12) # 6 interactions * 2 directions
        self.assertIn(('type_A', 6), patterns["most_frequent_interactions"])
        self.assertIn(('type_B', 6), patterns["most_frequent_interactions"])
        self.assertGreaterEqual(len(patterns["highly_connected_entities"]), 1)
        self.assertEqual(patterns["num_perceived_clusters"], 1) # All connected to observer
        self.assertIn("group1", patterns["perceived_groups"])
        self.assertEqual(patterns["perceived_groups"]["group1"], 2)
        self.assertIn("group2", patterns["perceived_groups"])
        self.assertEqual(patterns["perceived_groups"]["group2"], 2)

class TestUniverse(unittest.TestCase):
    def setUp(self):
        # Reset global variables before each test that uses persistent_interaction_rule
        universe_model.persistent_pair = None
        universe_model.persistent_interaction_count = 0

    def test_universe_creation(self):
        universe = Universe()
        self.assertEqual(universe.entities, [])
        self.assertEqual(universe.interaction_rules, [])

    def test_add_entity(self):
        universe = Universe()
        entity = Entity()
        universe.add_entity(entity)
        self.assertIn(entity, universe.entities)

    def test_add_interaction_rule(self):
        universe = Universe()
        def test_rule(entities): return []
        universe.add_interaction_rule(test_rule)
        self.assertIn(test_rule, universe.interaction_rules)

    def test_tick_generates_interactions(self):
        universe = Universe()
        entity1 = Entity()
        entity2 = Entity()
        universe.add_entity(entity1)
        universe.add_entity(entity2)
        universe.add_interaction_rule(gravity_rule)
        
        new_interactions = universe.tick()
        self.assertEqual(len(new_interactions), 1)
        self.assertEqual(new_interactions[0].interaction_type, "gravity")

    def test_scale_distance(self):
        self.assertAlmostEqual(scale_distance(0.1, 0.9), 0.2) 
        self.assertAlmostEqual(scale_distance(0.1, 0.2), 0.1)
        self.assertAlmostEqual(scale_distance(0.0, 1.0), 0.0)
        self.assertAlmostEqual(scale_distance(0.0, 0.5), 0.5)

    def test_scale_biased_encounter_rule(self):
        entities = [Entity(scale=0.1), Entity(scale=0.15), Entity(scale=0.9)]
        interactions = scale_biased_encounter_rule(entities)
        self.assertIsNotNone(interactions)
        self.assertEqual(len(interactions), 1)
        self.assertEqual(interactions[0].interaction_type, "scale_biased_encounter")

    def test_fusion_rule(self):
        e1 = Entity(scale=0.1)
        e2 = Entity(scale=0.12) 
        e3 = Entity(scale=0.8) 
        entities = [e1, e2, e3]

        interactions = fusion_rule(entities)
        self.assertIsNotNone(interactions)
        self.assertEqual(len(interactions), 1)
        self.assertEqual(interactions[0].interaction_type, "fusion")
        self.assertIn(e1, interactions[0].participants)
        self.assertIn(e2, interactions[0].participants)

    def test_group_formation_rule(self):
        universe = Universe()
        e1 = Entity()
        e2 = Entity()
        e3 = Entity()
        universe.add_entity(e1)
        universe.add_entity(e2)
        universe.add_entity(e3)

        # Custom rule to guarantee interactions between e1 and e2
        def guaranteed_interaction_rule(entities):
            if e1 in entities and e2 in entities:
                return [Interaction([e1, e2], interaction_type="guaranteed_bond")]
            return []
        universe.add_interaction_rule(guaranteed_interaction_rule)
        universe.add_interaction_rule(group_formation_rule) # Add the group formation rule

        # Run ticks to generate interactions
        for _ in range(2): # Run 2 ticks to ensure e1 and e2 interact twice
            universe.tick()

        # After ticks, check if a group_formed interaction occurred and its effects were applied
        found_group_formed_interaction = False
        for interaction in universe.interaction_history:
            if interaction.interaction_type == "group_formed":
                found_group_formed_interaction = True
                break
        self.assertTrue(found_group_formed_interaction)

        self.assertIsNotNone(e1.properties.get("group_id"))
        self.assertEqual(e1.properties["group_id"], e2.properties["group_id"])

    def test_persistent_interaction_rule(self):
        # Reset global state for this test
        global persistent_pair, persistent_interaction_count
        persistent_pair = None
        persistent_interaction_count = 0

        e1 = Entity()
        e2 = Entity()
        entities = [e1, e2]

        # Call the rule directly, as it manages its own global state
        interactions = persistent_interaction_rule(entities, max_interactions=2)
        self.assertEqual(len(interactions), 1)
        self.assertEqual(interactions[0].interaction_type, "persistent_bond")
        self.assertEqual(universe_model.persistent_interaction_count, 1)

        interactions = persistent_interaction_rule(entities, max_interactions=2)
        self.assertEqual(len(interactions), 1)
        self.assertEqual(interactions[0].interaction_type, "persistent_bond")
        self.assertEqual(universe_model.persistent_interaction_count, 2)

        interactions = persistent_interaction_rule(entities, max_interactions=2)
        self.assertIsNone(interactions) # Should stop after max_interactions
        self.assertEqual(universe_model.persistent_interaction_count, 2)

if __name__ == '__main__':
    unittest.main()