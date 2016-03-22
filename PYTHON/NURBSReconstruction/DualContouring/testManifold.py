import unittest
import extraction
import dcHelpers


class TestMesh(unittest.TestCase):
    def setUp(self):
        self.verts_coarse, self.quads_coarse, self.verts_fine, self.params = extraction.extract_surface('bridge',2)

    def test_bridge_has_no_manifold(self):
        edge_usage = dcHelpers.generate_edge_usage_dict(self.quads_coarse)
        for edge_identifier, used_by_quads in edge_usage.items():
            self.assertTrue(used_by_quads.__len__() == 2)

if __name__ == '__main__':
    unittest.main()
