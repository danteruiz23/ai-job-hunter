"""Quick checks for job URL allowlisting (run: python app/test_url_safety.py)."""

from app.services.job_search.url_safety import is_http_url_allowed


def main() -> None:
    assert is_http_url_allowed("https://example.com/jobs/123")
    assert not is_http_url_allowed("http://127.0.0.1/admin")
    assert not is_http_url_allowed("http://192.168.1.1/")
    assert not is_http_url_allowed("file:///etc/passwd")
    assert not is_http_url_allowed("http://localhost/x")
    assert not is_http_url_allowed("")
    print("url_safety OK")


if __name__ == "__main__":
    main()
