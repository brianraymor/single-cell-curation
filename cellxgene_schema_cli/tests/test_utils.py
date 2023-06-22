import pytest
from cellxgene_schema.utils import remove_deprecated_features, replace_ontology_term
from fixtures.examples_validate import adata, adata_non_raw


@pytest.fixture
def adata_with_raw():
    return adata.copy()


@pytest.fixture
def adata_without_raw():
    return adata_non_raw.copy()


@pytest.fixture
def deprecated_features():
    return ["ERCC-00002", "ENSG00000127603"]


@pytest.fixture
def deprecated_term_map_with_replacement_match():
    return {"EFO:0009899": "EFO:0000001"}


@pytest.fixture
def deprecated_term_map_no_replacement_match():
    return {"EFO:0000002": "EFO:0000003"}


def test_remove_deprecated_features__with_raw(adata_with_raw, deprecated_features):
    # Call the function under test
    result = remove_deprecated_features(adata_with_raw, deprecated_features)

    # Check if the deprecated features are removed
    assert result.var_names.tolist() == ["ENSMUSG00000059552", "ENSSASG00005000004"]
    assert result.raw.var_names.tolist() == ["ENSMUSG00000059552", "ENSSASG00005000004"]


def test_remove_deprecated_features__without_raw(adata_without_raw, deprecated_features):
    # Call the function under test
    result = remove_deprecated_features(adata_without_raw, deprecated_features)

    # Check if the deprecated features are removed
    assert result.var_names.tolist() == ["ENSMUSG00000059552", "ENSSASG00005000004"]
    assert result.raw is None


def test_replace_ontology_term__with_replacement(adata_with_raw, deprecated_term_map_with_replacement_match):
    replace_ontology_term(adata_with_raw.obs, "assay", deprecated_term_map_with_replacement_match)

    expected = ["EFO:0009918", "EFO:0000001"]
    actual = adata_with_raw.obs["assay_ontology_term_id"].dtype.categories
    assert all([a == b for a, b in zip(actual, expected)])


def test_replace_ontology_term__no_replacement(adata_with_raw, deprecated_term_map_no_replacement_match):
    replace_ontology_term(adata_with_raw.obs, "assay", deprecated_term_map_no_replacement_match)

    expected = ["EFO:0009899", "EFO:0009918"]
    actual = adata_with_raw.obs["assay_ontology_term_id"].dtype.categories
    assert all([a == b for a, b in zip(actual, expected)])