def test_graph(realm_context):
    graph = realm_context.dependency_graph
    name_to_proj = {p.name: p for p in realm_context.projects}
    names = [{proj.name for proj in level} for level in graph.topology]

    dep_a = name_to_proj["dep_a"]
    dep_b = name_to_proj["dep_b"]
    dep_c = name_to_proj["dep_c"]

    assert len(graph.topology) == 3, graph.topology
    assert names == [{"dep_c", "pkg", "pkg_with_groups"}, {"dep_b"}, {"dep_a"}]
    assert graph.project_deps[dep_b] == {dep_c}
    assert graph.projects_affected[dep_b] == {dep_a}
    assert graph.projects_affected[dep_c] == {dep_b}
