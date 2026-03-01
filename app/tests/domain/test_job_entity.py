def test_job_entity_creation(sample_job):
    assert sample_job.title == "Senior Python Developer"
    assert sample_job.company == "ACME Corp"
    assert sample_job.location == "Remote"
    assert sample_job.url.startswith("https://")