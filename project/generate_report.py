import csv
import matplotlib.pyplot as plt

def read_results(file_path):
    results = []
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append((row['Program'], row['Success'] == 'True'))
    return results

def generate_html(results, output_path):
    total = len(results)
    passed = sum(1 for _, success in results if success)
    failed = total - passed
    success_rate = (passed / total) * 100 if total > 0 else 0

    # HTML Content
    html = f"""
    <html>
    <head>
        <title>Repair Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            table {{ border-collapse: collapse; width: 60%; margin: 20px auto; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
            th {{ background-color: #4CAF50; color: white; }}
            .pass {{ background-color: #c8e6c9; }}
            .fail {{ background-color: #ffcdd2; }}
            h2 {{ text-align: center; }}
            .summary {{ text-align: center; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <h2>Repair Results Summary</h2>
        <div class="summary">
            <p>Total Programs: {total}</p>
            <p>Passed Repairs: {passed}</p>
            <p>Failed Repairs: {failed}</p>
            <p><strong>Success Rate: {success_rate:.2f}%</strong></p>
            <img src="pie_chart.png" width="300px">
        </div>
        <table>
            <tr><th>Program</th><th>Status</th></tr>
    """

    for name, success in results:
        status = "✓ Passed" if success else "✗ Failed"
        row_class = "pass" if success else "fail"
        html += f"<tr class='{row_class}'><td>{name}</td><td>{status}</td></tr>"

    html += "</table></body></html>"

    with open(output_path, 'w') as f:
        f.write(html)

def generate_chart(results, chart_path):
    passed = sum(1 for _, success in results if success)
    failed = len(results) - passed

    plt.figure(figsize=(4, 4))
    plt.pie([passed, failed], labels=["Passed", "Failed"], autopct="%1.1f%%", colors=["#81c784", "#e57373"])
    plt.title("Success Rate")
    plt.savefig(chart_path)
    plt.close()

if __name__ == "__main__":
    results = read_results("../results.csv")
    generate_chart(results, "../pie_chart.png")
    generate_html(results, "../report.html")
    print("✅ Report generated: ../report.html")
