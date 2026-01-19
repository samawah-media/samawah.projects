import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

class DataManager:
    def __init__(self):
        self.sheet_url = ""
        # We will try to use the Google Sheets connection if configured
        try:
            # Check if spreadsheet is configured in secrets
            if "connections" in st.secrets and "gsheets" in st.secrets.connections:
                self.conn = st.connection("gsheets", type=GSheetsConnection)
                self.use_gsheets = True
                # Store the sheet URL for display
                self.sheet_url = st.secrets.connections.gsheets.get("spreadsheet", "")
            else:
                self.use_gsheets = False
        except Exception:
            self.use_gsheets = False
            
        self.file_path = "mock_data.xlsx"

    def load_data(self, sheet_name):
        df = pd.DataFrame()
        if self.use_gsheets:
            try:
                # read() with worksheet name
                df = self.conn.read(worksheet=sheet_name)
            except Exception as e:
                # Fallback to local if Google Sheets fail
                try:
                    df = pd.read_excel(self.file_path, sheet_name=sheet_name)
                except:
                    df = pd.DataFrame()
        else:
            try:
                df = pd.read_excel(self.file_path, sheet_name=sheet_name)
            except:
                df = pd.DataFrame()
        
        # --- Normalize Columns ---
        # Map common variations to standard internal names
        column_map = {
            "Task_Name": "Task",
            "القسم": "Task",
            "المهمة": "Sub_Task",
            "Task_Category": "Category", # Optional, but good for consistency
        }
        if not df.empty:
            df = df.rename(columns=column_map)
            
        return df

    def get_project_stats(self, project_id):
        tasks_df = self.load_data("Tasks")
        if tasks_df.empty:
            return 0, 0, 0
            
        p_tasks = tasks_df[tasks_df['Project_ID'] == project_id]
        
        if p_tasks.empty:
            return 0, 0, 0
            
        total_qty = p_tasks['Quantity_Total'].sum()
        done_qty = p_tasks['Quantity_Done'].sum()
        
        progress = (done_qty / total_qty * 100) if total_qty > 0 else 0
        remaining_qty = total_qty - done_qty
        
        return round(progress, 1), int(total_qty), int(remaining_qty)

    def save_task_updates(self, df):
        if self.use_gsheets:
            try:
                # update() expects worksheet name and the dataframe
                self.conn.update(worksheet="Tasks", data=df)
                return True
            except Exception as e:
                st.error(f"Google Sheets update failed: {e}")
                return False
        else:
            try:
                with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    df.to_excel(writer, sheet_name="Tasks", index=False)
                return True
            except Exception as e:
                st.error(f"Local update failed: {e}")
                return False

    def get_config_list(self, config_type):
        """Returns a list of values for a specific type (e.g., Team_Member)"""
        try:
            config_df = self.load_data("Config")
            if config_df.empty:
                return []
            return config_df[config_df['Type'] == config_type]['Value'].tolist()
        except:
            return []

    def add_to_config(self, config_type, new_value):
        """Adds a new value to the config list"""
        config_df = self.load_data("Config")
        new_row = pd.DataFrame([{"Type": config_type, "Value": new_value}])
        updated_df = pd.concat([config_df, new_row], ignore_index=True)
        
        if self.use_gsheets:
            try:
                self.conn.update(worksheet="Config", data=updated_df)
                return True
            except Exception as e:
                st.error(f"Google Sheets config update failed: {e}")
                return False
        else:
            try:
                with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    updated_df.to_excel(writer, sheet_name="Config", index=False)
                return True
            except Exception:
                return False

    def save_meeting_recommendations(self, df):
        """Saves meeting recommendations to the MeetingRecommendations sheet"""
        if self.use_gsheets:
            try:
                self.conn.update(worksheet="MeetingRecommendations", data=df)
                return True
            except Exception as e:
                st.error(f"Google Sheets update failed: {e}")
                return False
        else:
            try:
                with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    df.to_excel(writer, sheet_name="MeetingRecommendations", index=False)
                return True
            except Exception as e:
                st.error(f"Local update failed: {e}")
                return False
