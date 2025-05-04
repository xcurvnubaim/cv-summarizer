import preprocessor
import util
import models
from config import Config
import time

summarizer_format = """
Summary: [Provide a concise 2-3 sentence overview]
Top Skills: [List up to 5 key skills, separated by semicolons]
Key Achievements: [List up to 3 achievements, separated by semicolons]
Education: [List highest degree and institution]
"""

def main():
    # Initialize the preprocessor
    config = Config()
    preprocessor_instance = preprocessor.CSVData('data/data-oprec.csv')
    cvmodel_instance = models.CVModel(config.API_KEY, config.MODEL_NAME)

    # util.download_all_cv(preprocessor_instance)

    # cv_summary_results = []
    # for i in range(preprocessor_instance.size()):
    #     row = preprocessor_instance.get_row(i)
    #     name = row['Nama']
    #     cv_path = f'data/cv/{name}.pdf'
    #     summarize_cv = cvmodel_instance.summarize_cv(cv_path, summarizer_format)

    #     # Parse the summarized content into separate fields
    #     summary_lines = summarize_cv.split("\n")
    #     summary_data = {
    #         'Nama': name,
    #         'Summary': util.extract_field(summary_lines, "Summary:"),
    #         'Top Skills': util.extract_field(summary_lines, "Top Skills:"),
    #         'Key Achievements': util.extract_field(summary_lines, "Key Achievements:"),
    #         'Education': util.extract_field(summary_lines, "Education:")
    #     }

    #     # Save results to a list
    #     cv_summary_results.append(summary_data)

    #     time.sleep(6)

    # # Save the results to a CSV file
    # output_file = 'data/cv_summary.csv'
    # util.summarize_cv_to_csv(cv_summary_results, output_file)

    data = util.extract_csv('data/cv_summary_1.csv')
    results = []
    
    for i, row in enumerate(data):
        if row['Top Skills'] == '':
            data_ori = preprocessor_instance.get_row(i)
            name = data_ori['Nama']
            cv_path = f'data/cv/{name}.pdf'
            summarize_cv = cvmodel_instance.summarize_cv(cv_path, summarizer_format)
            # print(summarize_cv)
            summary_lines = summarize_cv.split("\n")
            print(summary_lines)
            summary_data = {
                'Nama': name,
                'Summary': util.extract_field(summary_lines, "Summary:"),
                'Top Skills': util.extract_field(summary_lines, "Top Skills:"),
                'Key Achievements': util.extract_field(summary_lines, "Key Achievements:"),
                'Education': util.extract_field(summary_lines, "Education:")
            }
            print(summary_data)
            row['Summary'] = summary_data['Summary']
            row['Top Skills'] = summary_data['Top Skills']
            row['Key Achievements'] = summary_data['Key Achievements']
            row['Education'] = summary_data['Education']
            results.append(row)
            # time.sleep(6)
        else:
            results.append(row)
        
    # Save the updated results to a CSV file
    output_file = 'data/cv_summary.csv'
    util.summarize_cv_to_csv(results, output_file)

if __name__ == "__main__":
    main()