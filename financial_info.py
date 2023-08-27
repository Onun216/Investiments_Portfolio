import pandas as pd
import numpy as np

# Relevant Metrics
income_statement_metrics = ['Revenue', 'Gross Profit', 'Gross Margin %', 'Selling, General, & Admin. Expense',
                            'Research & Development', 'Total Operating Expense',
                            'Operating Income', 'Operating Margin %', 'Interest Income', 'Interest Expense',
                            'Net Income', 'Net Margin %', 'EPS (Diluted', 'Shares Outstanding (Diluted Average)',
                            'EBITDA', 'Depreciation, Depletion and Amortization']

balance_sheet_metrics = ['Cash and Cash Equivalents', 'Cash, Cash Equivalents, Marketable Securities',
                         'Accounts Receivable', 'Total Inventories', 'Total Current Assets',
                         'Gross Property, Plant and Equipment', 'Intangible Assets', 'Goodwill',
                         'Total Long-Term Assets', 'Total Assets', 'Accounts Payable', 'Long-Term Debt',
                         'Long-Term Debt & Capital Lease Obligation', 'Debt-to-Equity',
                         'Pension And Retirement Benefit',
                         'Total Liabilities', 'Preferred Stock', 'Retained Earnings', 'Treasury Stock',
                         'Total Stockholders Equity']

cashflow_statement_metrics = ['Change In Inventory', 'Stock Based Compensation', 'Cash Flow from Operations',
                              'Purchase Of Property, Plant, Equipment', 'Sale Of Property, Plant, Equipment',
                              'Purchase Of Business', 'Sale Of Business', 'Purchase Of Investment',
                              'Sale Of Investment',
                              'Issuance of Stock', 'Repurchase of Stock', 'Issuance of Debt', 'Payments of Debt',
                              'Cash Flow from Financing', 'Effect of Exchange Rate Changes', 'Capital Expenditure',
                              'Free Cash Flow']

valuation_ratios_metrics = ['PE Ratio', 'Price-to-Owner-Earnings', 'PB Ratio', 'Price-to-Tangible-Book',
                            'Price-to-Free-Cash-Flow', 'Price-to-Operating-Cash-Flow', 'PS Ratio', 'PEG Ratio',
                            'EV-to-Revenue', 'EV-to-EBITDA', 'Dividend Yield %']

per_share_metrics = ['EBIT per Share', 'Earnings per Share (Diluted)', 'Cash per Share', 'Dividends per Share',
                     'Book Value per Share', 'Tangible Book per Share', 'Total Debt per Share']

common_size_ratios = ['ROE %', 'ROA %', 'Return-on-Tangible-Asset', 'ROIC %', 'WACC %',
                      'Effective Interest Rate on Debt %',
                      'Gross Margin %', 'Operating Margin %', 'Net Margin %', 'EBITDA Margin %', 'FCF Margin %',
                      'Debt-to-Equity', 'Inventory Turnover', 'COGS-to-Revenue', 'Inventory-to-Revenue',
                      'Capex-to-Revenue',
                      'Capex-to-Operating-Income', 'Capex-to-Operating-Cash-Flow']

# Convert table into dataframe
table = dict({'per_share_data_array': np.array(per_share_metrics), 'common_size_ratios': np.array(common_size_ratios),
              'income_statement': np.array(income_statement_metrics), 'balance_sheet': np.array(balance_sheet_metrics),
              'cashflow_statement': np.array(cashflow_statement_metrics),
              'valuation_ratios': np.array(valuation_ratios_metrics)})

df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in table.items()]))


# Show available categories and metrics for chosen category
def gf_choose_metric():
    print('Categorias disponíveis para pesquisa:')
    for keys in table.keys():
        print(keys)

    cat = input('\nInsira uma categoria: ')
    print('\nMétricas disponíveis para pesquisa: ')
    for metric in table[cat]:
        print(metric)

    metric = input('\nInsira uma métrica: ')
    return cat, metric
