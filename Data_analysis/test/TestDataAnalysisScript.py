import Data_analysis.DataAnalysisScript

from Data_analysis.DataAnalysisScript import DataAnalyzer
def main():
    # Ask for the CSV file path
    file_path = input("Enter the path to the CSV file: ")

    # Create an instance of DataAnalyzer with the file path
    analyzer = DataAnalyzer(file_path)

    # Get analysis results
    results = analyzer.analyze_data()

    # Print the results
    for key, value in results.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
