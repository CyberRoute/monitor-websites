from src.monitor import Monitor


class TestMonitor:

    def test_is_alive(self):
        obj = Monitor()
        result = obj.is_alive("www.google.com")
        expected = True
        assert result == expected

    def test_is_alive_false(self):
        obj = Monitor()
        result = obj.is_alive("www.hjkfdahjk.com")
        expected = False
        assert result == expected

    def test_get_statuses_200(self):
        obj = Monitor()
        result = obj.get_statuses("http://www.google.com")
        assert result[0] == 200
        assert len(result) == 4

    def test_get_statuses_error(self):
        obj = Monitor()
        result = obj.get_statuses("http://www.hjkfdhjskfds.com")
        assert result == "UNREACHABLE"

    def test_check_single_url(self):
        obj = Monitor()
        result = obj.check_single_url("http://www.google.com")
        assert result[0] == 200
        assert len(result) == 4

    def test_check_single_url_error(self):
        obj = Monitor()
        result = obj.check_single_url("http://www.hjkfdsahjkfhjka.com")
        assert result == "UNREACHABLE"

    def test_https_start_strip(self):
        obj = Monitor()
        result = obj.https_start_strip("http://www.google.com")
        expected = "http://www.google.com"
        result_https = obj.https_start_strip("https://www.google.com")
        expected_https = "https://www.google.com"
        result_else = obj.https_start_strip("www.google.com")
        assert result == expected
        assert result_https == expected_https
        assert result_else == expected_https

    def test_generate_list_urls(self):
        data = {
        "Salesforce": [
                "https://www.salesforce.com",
                "http://www.salesforce.com"
        ],
        "Google": [
                "https://www.google.com",
                "http://www.google.com"
        ],
        "Amazon": [
                "https://www.amazon.it",
                "http://www.amazon.it"
        ],
        "CNN": [
                "https://www.cnn.com",
                "http://www.cnn.com"
        ]
        }
        obj = Monitor()
        result = obj.generate_list_urls(data)
        assert len(result) == 8
        assert result[0] == "https://www.salesforce.com"

