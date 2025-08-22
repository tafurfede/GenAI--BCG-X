"""
Financial Analysis Chatbot Prototype
A simple chatbot that responds to predefined financial queries based on analyzed SEC 10-K data
"""

import pandas as pd
import os

class FinancialChatbot:
    def __init__(self):
        """Initialize the chatbot with financial data"""
        self.load_financial_data()
        self.setup_responses()
        
    def load_financial_data(self):
        """Load the analyzed financial data"""
        # Check if we're in Task 1 folder or parent directory
        if os.path.exists('financial_data_sample.csv'):
            data_path = 'financial_data_sample.csv'
        elif os.path.exists('Task 1/financial_data_sample.csv'):
            data_path = 'Task 1/financial_data_sample.csv'
        else:
            # Use embedded sample data if file not found
            self.use_embedded_data()
            return
            
        self.df = pd.read_csv(data_path)
        self.prepare_data()
    
    def use_embedded_data(self):
        """Use embedded sample data if CSV not found"""
        data = {
            'Company': ['Microsoft', 'Microsoft', 'Microsoft', 'Tesla', 'Tesla', 'Tesla', 'Apple', 'Apple', 'Apple'],
            'Year': [2022, 2023, 2024, 2022, 2023, 2024, 2022, 2023, 2024],
            'Total Revenue': [198270, 211915, 245122, 53823, 81462, 96773, 365817, 394328, 383285],
            'Net Income': [72738, 72361, 88136, 5519, 12556, 14997, 94680, 99803, 94749],
            'Total Assets': [364840, 411976, 512163, 62131, 82330, 106618, 381191, 365725, 352755],
            'Total Liabilities': [198298, 205753, 243686, 26709, 36440, 43015, 287912, 279414, 258549],
            'Cash Flow from Operating Activities': [89035, 87582, 118291, 7054, 11497, 13643, 104038, 122151, 99829]
        }
        self.df = pd.DataFrame(data)
        self.prepare_data()
    
    def prepare_data(self):
        """Prepare data for chatbot responses"""
        # Calculate growth rates
        self.df['Revenue Growth (%)'] = self.df.groupby('Company')['Total Revenue'].pct_change() * 100
        self.df['Net Income Growth (%)'] = self.df.groupby('Company')['Net Income'].pct_change() * 100
        
        # Calculate profit margins
        self.df['Profit Margin (%)'] = (self.df['Net Income'] / self.df['Total Revenue']) * 100
        
        # Get latest year data
        self.latest_year = self.df['Year'].max()
        self.latest_data = self.df[self.df['Year'] == self.latest_year]
        
    def setup_responses(self):
        """Setup predefined responses based on financial data"""
        # Calculate total revenue for all companies in latest year
        total_revenue = self.latest_data['Total Revenue'].sum()
        
        # Find company with highest revenue
        revenue_leader = self.latest_data.loc[self.latest_data['Total Revenue'].idxmax(), 'Company']
        revenue_leader_amount = self.latest_data.loc[self.latest_data['Total Revenue'].idxmax(), 'Total Revenue']
        
        # Calculate average net income change
        income_changes = []
        for company in self.df['Company'].unique():
            company_data = self.df[self.df['Company'] == company].sort_values('Year')
            if len(company_data) >= 2:
                last_income = company_data.iloc[-1]['Net Income']
                prev_income = company_data.iloc[-2]['Net Income']
                change = ((last_income - prev_income) / prev_income) * 100
                income_changes.append((company, change))
        
        # Store responses
        self.responses = {
            "total revenue": f"The combined total revenue for all three companies in {self.latest_year} is ${total_revenue:,.0f} million.",
            
            "net income change": self._format_income_changes(income_changes),
            
            "profit margin": self._format_profit_margins(),
            
            "revenue leader": f"{revenue_leader} has the highest revenue in {self.latest_year} with ${revenue_leader_amount:,.0f} million.",
            
            "financial health": self._format_financial_health()
        }
    
    def _format_income_changes(self, income_changes):
        """Format net income changes response"""
        response = f"Net income changes from {self.latest_year-1} to {self.latest_year}:\n"
        for company, change in income_changes:
            direction = "increased" if change > 0 else "decreased"
            response += f"- {company}: {direction} by {abs(change):.1f}%\n"
        return response.strip()
    
    def _format_profit_margins(self):
        """Format profit margins response"""
        response = f"Profit margins for {self.latest_year}:\n"
        for _, row in self.latest_data.iterrows():
            margin = (row['Net Income'] / row['Total Revenue']) * 100
            response += f"- {row['Company']}: {margin:.1f}%\n"
        return response.strip()
    
    def _format_financial_health(self):
        """Format financial health response"""
        response = "Financial health assessment based on debt-to-assets ratio:\n"
        for _, row in self.latest_data.iterrows():
            ratio = row['Total Liabilities'] / row['Total Assets']
            health = "Strong" if ratio < 0.5 else "Moderate" if ratio < 0.7 else "Leveraged"
            response += f"- {row['Company']}: {health} (ratio: {ratio:.2f})\n"
        return response.strip()
    
    def simple_chatbot(self, user_query):
        """Main chatbot function that processes user queries"""
        # Convert query to lowercase for matching
        query_lower = user_query.lower()
        
        # Check for predefined queries
        if "total revenue" in query_lower:
            return self.responses["total revenue"]
        
        elif "net income" in query_lower and ("change" in query_lower or "year" in query_lower):
            return self.responses["net income change"]
        
        elif "profit margin" in query_lower:
            return self.responses["profit margin"]
        
        elif "highest revenue" in query_lower or "revenue leader" in query_lower:
            return self.responses["revenue leader"]
        
        elif "financial health" in query_lower or "debt" in query_lower:
            return self.responses["financial health"]
        
        else:
            return ("Sorry, I can only provide information on predefined queries:\n"
                   "- 'What is the total revenue?'\n"
                   "- 'How has net income changed over the last year?'\n"
                   "- 'What are the profit margins?'\n"
                   "- 'Which company has the highest revenue?'\n"
                   "- 'How is the financial health of the companies?'")
    
    def run_interactive(self):
        """Run the chatbot in interactive mode"""
        print("=" * 60)
        print("Financial Analysis Chatbot")
        print("=" * 60)
        print("Welcome! I can answer questions about Microsoft, Tesla, and Apple's financials.")
        print("Type 'quit' to exit.\n")
        
        print("Available queries:")
        print("- What is the total revenue?")
        print("- How has net income changed over the last year?")
        print("- What are the profit margins?")
        print("- Which company has the highest revenue?")
        print("- How is the financial health of the companies?")
        print("-" * 60)
        
        while True:
            user_input = input("\nYour question: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Thank you for using the Financial Analysis Chatbot. Goodbye!")
                break
            
            response = self.simple_chatbot(user_input)
            print(f"\nChatbot: {response}")


if __name__ == "__main__":
    # Run in interactive command-line mode
    chatbot = FinancialChatbot()
    chatbot.run_interactive()