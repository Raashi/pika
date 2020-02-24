from sources import startups

for startup in startups:
    startup.apply_async()
