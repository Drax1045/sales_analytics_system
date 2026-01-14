from datetime import datetime
from collections import defaultdict

# Import analytics utilities
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)


def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """
    Generates a comprehensive formatted sales analytics report and
    writes it to a text file.
    """

    # =========================
    # HEADER SECTION
    # =========================
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_records = len(transactions)

    with open(output_file, "w") as f:
        f.write("=" * 45 + "\n")
        f.write("SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {now}\n")
        f.write(f"Records Processed: {total_records}\n")
        f.write("=" * 45 + "\n\n")

        # =========================
        # OVERALL SUMMARY
        # =========================
        total_revenue = calculate_total_revenue(transactions)
        total_transactions = len(transactions)
        avg_order_value = total_revenue / total_transactions if total_transactions else 0

        dates = sorted(tx["Date"] for tx in transactions)
        date_range = f"{dates[0]} to {dates[-1]}"

        f.write("OVERALL SUMMARY\n")
        f.write("-" * 45 + "\n")
        f.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {total_transactions}\n")
        f.write(f"Average Order Value: ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range: {date_range}\n\n")

        # =========================
        # REGION-WISE PERFORMANCE
        # =========================
        region_stats = region_wise_sales(transactions)

        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 45 + "\n")
        f.write(f"{'Region':<10}{'Sales':>12}{'% of Total':>15}{'Transactions':>15}\n")

        for region, data in region_stats.items():
            f.write(
                f"{region:<10}₹{data['total_sales']:>10,.0f}"
                f"{data['percentage']:>14.2f}%"
                f"{data['transaction_count']:>15}\n"
            )
        f.write("\n")

        # =========================
        # TOP 5 PRODUCTS
        # =========================
        top_products = top_selling_products(transactions)[:5]

        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 45 + "\n")
        f.write(f"{'Rank':<6}{'Product':<20}{'Qty':>6}{'Revenue':>12}\n")

        for i, (name, qty, rev) in enumerate(top_products, 1):
            f.write(f"{i:<6}{name:<20}{qty:>6}₹{rev:>10,.0f}\n")
        f.write("\n")

        # =========================
        # TOP 5 CUSTOMERS
        # =========================
        customers = list(customer_analysis(transactions).items())[:5]

        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 45 + "\n")
        f.write(f"{'Rank':<6}{'Customer':<12}{'Spent':>12}{'Orders':>10}\n")

        for i, (cid, data) in enumerate(customers, 1):
            f.write(
                f"{i:<6}{cid:<12}₹{data['total_spent']:>10,.0f}"
                f"{data['purchase_count']:>10}\n"
            )
        f.write("\n")

        # =========================
        # DAILY SALES TREND
        # =========================
        daily = daily_sales_trend(transactions)

        f.write("DAILY SALES TREND\n")
        f.write("-" * 45 + "\n")
        f.write(f"{'Date':<12}{'Revenue':>12}{'Txns':>8}{'Customers':>12}\n")

        for date, d in daily.items():
            f.write(
                f"{date:<12}₹{d['revenue']:>10,.0f}"
                f"{d['transaction_count']:>8}"
                f"{d['unique_customers']:>12}\n"
            )
        f.write("\n")

        # =========================
        # PRODUCT PERFORMANCE ANALYSIS
        # =========================
        best_day = find_peak_sales_day(transactions)
        low_products = low_performing_products(transactions)

        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 45 + "\n")
        f.write(f"Best Selling Day: {best_day[0]} | Revenue: ₹{best_day[1]:,.0f}\n")

        if low_products:
            f.write("Low Performing Products:\n")
            for p in low_products:
                f.write(f"- {p[0]} (Qty: {p[1]}, Revenue: ₹{p[2]:,.0f})\n")
        else:
            f.write("No low performing products found.\n")

        f.write("\n")

        # =========================
        # API ENRICHMENT SUMMARY
        # =========================
        total_enriched = sum(1 for tx in enriched_transactions if tx.get("API_Match"))
        success_rate = (
            (total_enriched / len(enriched_transactions)) * 100
            if enriched_transactions else 0
        )

        failed_products = sorted(
            set(tx["ProductName"] for tx in enriched_transactions if not tx.get("API_Match"))
        )

        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 45 + "\n")
        f.write(f"Total products enriched: {total_enriched}\n")
        f.write(f"Success rate: {success_rate:.2f}%\n")

        if failed_products:
            f.write("Products not enriched:\n")
            for p in failed_products:
                f.write(f"- {p}\n")
        else:
            f.write("All products successfully enriched.\n")
