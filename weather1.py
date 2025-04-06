import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import random
from datetime import datetime, timedelta
# Database for soil, crops, and fertilizers
soil_data = {
    "Loamy": {
        "description": "Well-balanced soil with good drainage and nutrient retention",
        "pH_range": (6.0, 7.0),
        "moisture_retention": "High"
    },
    "Clay": {
        "description": "Heavy soil with poor drainage but high nutrient content",
        "pH_range": (5.5, 6.5),
        "moisture_retention": "Very High"
    },
    "Sandy": {
        "description": "Light soil with excellent drainage but low nutrient retention",
        "pH_range": (5.0, 6.5),
        "moisture_retention": "Low"
    },
    "Silty": {
        "description": "Smooth texture with moderate drainage and good fertility",
        "pH_range": (6.0, 7.5),
        "moisture_retention": "Moderate"
    }
}

crop_recommendations = {
    "Loamy": ["Tomatoes", "Carrots", "Lettuce", "Cucumbers", "Peppers"],
    "Clay": ["Potatoes", "Rice", "Cabbage", "Broccoli", "Brussels Sprouts"],
    "Sandy": ["Corn", "Barley", "Watermelons", "Sweet Potatoes", "Asparagus"],
    "Silty": ["Wheat", "Oats", "Soybeans", "Spinach", "Strawberries"]
}

fertilizer_recommendations = {
    "Tomatoes": {"N-P-K": "5-10-10", "Organic": "Compost + Bone Meal"},
    "Carrots": {"N-P-K": "1-2-2", "Organic": "Well-rotted manure"},
    "Lettuce": {"N-P-K": "10-10-10", "Organic": "Fish emulsion"},
    "Potatoes": {"N-P-K": "15-15-15", "Organic": "Compost + Wood Ash"},
    "Corn": {"N-P-K": "16-16-8", "Organic": "Composted chicken manure"},
    # Add more crops and their fertilizer needs
}

def get_weather(location, days=5):
    """Generate simulated weather data for multiple days"""
    weather_conditions = ["Sunny", "Rainy", "Cloudy", "Partly Cloudy", "Stormy"]
    forecast = []
    
    for i in range(days):
        date = datetime.now() + timedelta(days=i)
        temperature = random.randint(15, 35)
        condition = random.choice(weather_conditions)
        humidity = random.randint(30, 90)
        wind_speed = random.randint(5, 20)
        rain_chance = random.randint(0, 100) if condition in ["Rainy", "Stormy"] else random.randint(0, 30)
        
        forecast.append({
            "date": date.strftime("%Y-%m-%d"),
            "temperature": temperature,
            "condition": condition,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "rain_chance": rain_chance
        })
    
    return forecast

def get_soil_recommendations(soil_type, ph_level):
    """Get crop recommendations based on soil type and pH"""
    crops = crop_recommendations.get(soil_type, [])
    
    # Filter crops based on pH tolerance (simplified)
    ph_tolerant_crops = []
    for crop in crops:
        # In a real system, we'd have specific pH ranges for each crop
        if 5.5 <= ph_level <= 7.5:  # Most crops tolerate this range
            ph_tolerant_crops.append(crop)
    
    return ph_tolerant_crops

def get_fertilizer_recommendation(crop):
    """Get fertilizer recommendations for a specific crop"""
    return fertilizer_recommendations.get(crop, {"N-P-K": "10-10-10", "Organic": "General purpose compost"})

def ai_chat_response(user_input):
    """Simple AI chatbot response system"""
    user_input = user_input.lower()
    
    responses = {
        "hello": "Hello! How can I assist you with your farming needs today?",
        "hi": "Hi there! What agricultural advice are you looking for?",
        "weather": "I can provide weather forecasts. Please enter your location.",
        "soil": "I can analyze soil and recommend crops. What's your soil type?",
        "crop": "I can suggest crops based on your soil. What soil type do you have?",
        "fertilizer": "I can recommend fertilizers. Which crop are you growing?",
        "bye": "Goodbye! Happy farming!",
        "thanks": "You're welcome! Let me know if you need more help."
    }
    
    for key in responses:
        if key in user_input:
            return responses[key]
    
    return "I'm not sure I understand. Could you ask about weather, soil, crops, or fertilizers?"

class AgriculturalAdvisoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Agricultural Advisory System")
        self.root.geometry("800x600")
        
        # Create tabs
        self.tab_control = ttk.Notebook(root)
        
        # Weather Tab
        self.weather_tab = ttk.Frame(self.tab_control)
        self.setup_weather_tab()
        
        # Soil Analysis Tab
        self.soil_tab = ttk.Frame(self.tab_control)
        self.setup_soil_tab()
        
        # Chatbot Tab
        self.chat_tab = ttk.Frame(self.tab_control)
        self.setup_chat_tab()
        
        self.tab_control.add(self.weather_tab, text="Weather Forecast")
        self.tab_control.add(self.soil_tab, text="Soil Analysis")
        self.tab_control.add(self.chat_tab, text="AI Chatbot")
        self.tab_control.pack(expand=1, fill="both")
    
    def setup_weather_tab(self):
        # Location Entry
        tk.Label(self.weather_tab, text="Location:").grid(row=0, column=0, padx=10, pady=5)
        self.location_entry = tk.Entry(self.weather_tab, width=30)
        self.location_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Days to forecast
        tk.Label(self.weather_tab, text="Days to forecast:").grid(row=1, column=0, padx=10, pady=5)
        self.days_entry = tk.Spinbox(self.weather_tab, from_=1, to=10, width=5)
        self.days_entry.grid(row=1, column=1, padx=10, pady=5)
        self.days_entry.delete(0, "end")
        self.days_entry.insert(0, "5")
        
        # Get Weather Button
        self.weather_btn = tk.Button(self.weather_tab, text="Get Weather Forecast", command=self.show_weather)
        self.weather_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Weather Results
        self.weather_results = scrolledtext.ScrolledText(self.weather_tab, width=70, height=20)
        self.weather_results.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    
    def setup_soil_tab(self):
        # Soil Type
        tk.Label(self.soil_tab, text="Soil Type:").grid(row=0, column=0, padx=10, pady=5)
        self.soil_type_var = tk.StringVar()
        self.soil_type_menu = ttk.Combobox(self.soil_tab, textvariable=self.soil_type_var, 
                                         values=list(soil_data.keys()))
        self.soil_type_menu.grid(row=0, column=1, padx=10, pady=5)
        self.soil_type_menu.current(0)
        
        # pH Level
        tk.Label(self.soil_tab, text="pH Level:").grid(row=1, column=0, padx=10, pady=5)
        self.ph_entry = tk.Entry(self.soil_tab, width=10)
        self.ph_entry.grid(row=1, column=1, padx=10, pady=5)
        self.ph_entry.insert(0, "6.5")
        
        # Analyze Button
        self.analyze_btn = tk.Button(self.soil_tab, text="Analyze Soil", command=self.analyze_soil)
        self.analyze_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Soil Results
        self.soil_results = scrolledtext.ScrolledText(self.soil_tab, width=70, height=20)
        self.soil_results.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    
    def setup_chat_tab(self):
        # Chat History
        self.chat_history = scrolledtext.ScrolledText(self.chat_tab, width=70, height=20, state='disabled')
        self.chat_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        # User Input
        self.user_input = tk.Entry(self.chat_tab, width=50)
        self.user_input.grid(row=1, column=0, padx=10, pady=5)
        
        # Send Button
        self.send_btn = tk.Button(self.chat_tab, text="Send", command=self.process_chat_input)
        self.send_btn.grid(row=1, column=1, padx=10, pady=5)
        
        # Bind Enter key to send message
        self.user_input.bind("<Return>", lambda event: self.process_chat_input())
        
        # Initial greeting
        self.update_chat_history("AI: Hello! I'm your agricultural assistant. How can I help you today?")
    
    def show_weather(self):
        location = self.location_entry.get()
        if not location:
            messagebox.showerror("Error", "Please enter a location")
            return
        
        try:
            days = int(self.days_entry.get())
            if days < 1 or days > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a number between 1 and 10 for days")
            return
        
        weather_data = get_weather(location, days)
        
        result_text = f"Weather Forecast for {location}:\n\n"
        for day in weather_data:
            result_text += (
                f"Date: {day['date']}\n"
                f"Condition: {day['condition']}\n"
                f"Temperature: {day['temperature']}°C\n"
                f"Humidity: {day['humidity']}%\n"
                f"Wind Speed: {day['wind_speed']} km/h\n"
                f"Rain Chance: {day['rain_chance']}%\n"
                f"{'-'*30}\n"
            )
        
        self.weather_results.delete(1.0, tk.END)
        self.weather_results.insert(tk.INSERT, result_text)
        
        # Add agricultural advice based on weather
        advice = self.generate_weather_advice(weather_data)
        self.weather_results.insert(tk.END, "\nAgricultural Advice:\n" + advice)
    
    def generate_weather_advice(self, weather_data):
        """Generate farming advice based on weather forecast"""
        advice = []
        rainy_days = sum(1 for day in weather_data if day['condition'] in ["Rainy", "Stormy"])
        max_temp = max(day['temperature'] for day in weather_data)
        min_temp = min(day['temperature'] for day in weather_data)
        
        if rainy_days >= 3:
            advice.append("- Expect significant rainfall. Consider delaying irrigation and ensure proper drainage.")
        if max_temp > 30:
            advice.append("- High temperatures expected. Increase watering frequency for sensitive crops.")
        if min_temp < 18:
            advice.append("- Cool temperatures expected. Protect sensitive seedlings if necessary.")
        
        return "\n".join(advice) if advice else "- Weather conditions look favorable for most crops."
    
    def analyze_soil(self):
        soil_type = self.soil_type_var.get()
        try:
            ph_level = float(self.ph_entry.get())
            if ph_level < 0 or ph_level > 14:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid pH level between 0 and 14")
            return
        
        # Get soil information
        soil_info = soil_data.get(soil_type, {})
        
        # Get crop recommendations
        crops = get_soil_recommendations(soil_type, ph_level)
        
        # Build result text
        result_text = (
            f"Soil Analysis Results:\n\n"
            f"Soil Type: {soil_type}\n"
            f"Description: {soil_info.get('description', 'N/A')}\n"
            f"Optimal pH Range: {soil_info.get('pH_range', (0, 14))}\n"
            f"Your pH Level: {ph_level}\n"
            f"Moisture Retention: {soil_info.get('moisture_retention', 'N/A')}\n\n"
            f"Recommended Crops:\n"
        )
        
        for crop in crops:
            fertilizer = get_fertilizer_recommendation(crop)
            result_text += (
                f"- {crop}\n"
                f"  Fertilizer Recommendation:\n"
                f"  Synthetic: {fertilizer['N-P-K']}\n"
                f"  Organic: {fertilizer['Organic']}\n\n"
            )
        
        # pH advice
        optimal_min, optimal_max = soil_info.get('pH_range', (6.0, 7.0))
        if ph_level < optimal_min:
            result_text += f"\nYour soil is too acidic (pH {ph_level}). Consider adding lime to raise pH."
        elif ph_level > optimal_max:
            result_text += f"\nYour soil is too alkaline (pH {ph_level}). Consider adding sulfur to lower pH."
        else:
            result_text += "\nYour soil pH is in the optimal range for most crops."
        
        self.soil_results.delete(1.0, tk.END)
        self.soil_results.insert(tk.INSERT, result_text)
    
    def process_chat_input(self):
        user_message = self.user_input.get()
        if not user_message:
            return
        
        self.update_chat_history(f"You: {user_message}")
        self.user_input.delete(0, tk.END)
        
        # Simple AI response
        ai_response = ai_chat_response(user_message)
        self.update_chat_history(f"AI: {ai_response}")
        
        # Handle specific queries that require data from other tabs
        if "weather" in user_message.lower():
            location = self.location_entry.get()
            if location:
                weather_data = get_weather(location, 3)
                summary = f"Weather in {location}: {weather_data[0]['condition']}, {weather_data[0]['temperature']}°C"
                self.update_chat_history(f"AI: {summary}")
            else:
                self.update_chat_history("AI: Please enter your location in the Weather tab first.")
        
        elif "crop" in user_message.lower() and "soil" in user_message.lower():
            soil_type = self.soil_type_var.get()
            crops = crop_recommendations.get(soil_type, [])
            if crops:
                self.update_chat_history(f"AI: For {soil_type} soil, recommended crops are: {', '.join(crops)}")
            else:
                self.update_chat_history("AI: Please select your soil type in the Soil Analysis tab first.")
    
    def update_chat_history(self, message):
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, message + "\n\n")
        self.chat_history.config(state='disabled')
        self.chat_history.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = AgriculturalAdvisoryApp(root)
    root.mainloop()
