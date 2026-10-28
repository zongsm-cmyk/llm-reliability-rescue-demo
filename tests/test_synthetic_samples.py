from examples.jsonl_samples import samples


def test_sample_count():
    assert len(samples()) == 4
