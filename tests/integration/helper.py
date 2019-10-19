async def _client_get(app, ufs):
    client = app.test_client()
    response = await client.get(ufs, headers=[("Accept-Encoding", "gzip")])
    assert response.status_code == 200

    return response
