import unittest


class VerboseTextTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_file = None

    def startTestRun(self):
        super().startTestRun()
        print("Running tests...\n")

    def startTest(self, test):
        super().startTest(test)
        if self.current_file != test.id().split(".")[1]:
            self.current_file = test.id().split(".")[1]
            print(f"\nRunning tests from file: {self.current_file}")


if __name__ == "__main__":
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("test", pattern="test_*.py", top_level_dir="test")

    runner = unittest.TextTestRunner(resultclass=VerboseTextTestResult)
    result = runner.run(test_suite)
