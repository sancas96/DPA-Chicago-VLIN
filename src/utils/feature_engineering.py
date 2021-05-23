import pandas as pd
from sklearn.preprocessing import LabelEncoder 

class FeatureEngineering():
    def __init__(self, dataframe):
        self.dataframe = dataframe
  
    def feature_engineering(self):
        def split_inf(violations):
            values_row = pd.Series([])
            if type(violations) == str:
                violations = violations.split(' | ')
                for violation in violations:
                    index = "v_" + violation.split('.')[0]
                    values_row[index] = 1
            return values_row
                
        values_data = self.dataframe.violations.apply(split_inf).fillna(0)
        critical_cols = [("v_" + str(num)) for num in range(1, 15)]
        serious_cols = [("v_" + str(num)) for num in range(15, 30)]
        minor_cols = [("v_" + str(num)) for num in range(30, 45)]
        minor_cols.append("v_70")
        columns = critical_cols + serious_cols + minor_cols
        values = pd.DataFrame(values_data, columns=columns)
        values['inspection_id'] = self.dataframe['inspection_id']
        titles = pd.DataFrame({
                'v_1': 'Approved_food_sources_1',
                'v_2': 'Hot_cold_storage_facilities_2',
                'v_3': 'Hot_cold_storage_temp}_3',
                'v_4': 'Contaminant_protection_4',
                'v_5': 'No_sick_handlers_5',
                'v_6': 'Proper_hand_washing_6',
                'v_7': 'Proper_utensil_washing_7',
                'v_8': 'Proper_sanitizing_solution_8',
                'v_9': 'Hot_cold_water_supply_9',
                'v_10': 'Waste_water_disposal_10',
                'v_11': 'Adequate_toilet_facilities_11',
                'v_12': 'Adequate_hand_washing_facilities_12',
                'v_13': 'Control_of_rodents_other_pests_13',
                'v_14': 'Correct_serious_violations_14',
                'v_15': 'No_reserved_food_15',
                'v_16': 'Protection_from_contamination_16',
                'v_17': 'Proper_thawing_17',
                'v_18': 'Pest_control_associated_areas_18',
                'v_19': 'Proper_garbage_area_19',
                'v_20': 'Proper_garbage_storage_20',
                'v_21': 'Oversight_of_hazardous_food_21',
                'v_22': 'Dishwasher_maintenance_22',
                'v_23': 'Scrape_before_washing_23',
                'v_24': 'Proper_dishwashers_24',
                'v_25': 'Minimize_toxic_materials_25',
                'v_26': 'Adequate_customer_toilets_26',
                'v_27': 'Supplied_toilet_facilities_27',
                'v_28': 'Visible_inspection_report_28',
                'v_29': 'Correct_minor_violations_29',
                'v_30': 'Labelled_containers_30',
                'v_31': 'Sterile_utensils_31',
                'v_32': 'Clean_maintain_equipment_32',
                'v_33': 'Clean_sanitize_utensils_33',
                'v_34': 'Clean_maintain_floor_34',
                'v_35': 'Maintain_walls_ceiling_35',
                'v_36': 'Proper_lighting_36',
                'v_37': 'Toilet_rooms_vented_37',
                'v_38': 'Proper_venting_plumbing_38',
                'v_39': 'Linen_clothing_storage_39',
                'v_40': 'Proper_thermometers_40',
                'v_41': 'Clean_facilities_store_supplies_41',
                'v_42': 'Ice_handling_hairnets_clothes_42',
                'v_43': 'Ice_equipment_storage_43',
                'v_44': 'Restrict_prep_area_traffic_44',
                'v_70': 'Restrict_smoking_70'
            }, index=[0])
        counts = pd.DataFrame({
            "critical_count": values[critical_cols].sum(axis=1),
            "serious_count": values[serious_cols].sum(axis=1),
            "minor_count": values[minor_cols].sum(axis=1)
            })
        counts['inspection_id'] = self.dataframe['inspection_id']
        titled_values = values.rename(columns=titles.iloc[0])
        train = pd.merge(self.dataframe, titled_values, on='inspection_id')
        train = pd.merge(train, counts, on='inspection_id')
        le = LabelEncoder() 
        train['dba_name'] = le.fit_transform(train['dba_name'])
        train['facility_type'] = train['facility_type'].astype(str)
        #train['facility_type'] = le.fit_transform(train['facility_type'])
        train['address'] = le.fit_transform(train['address'])
        train['zip'] = le.fit_transform(train['zip'])
        train['results'] = (train['results'].values == 'Fail').astype('int')
        train['risk'] = train['risk'].astype(str)
        train['risk'] = le.fit_transform(train['risk'])
        train = train.drop(['aka_name', 'city', 'state', 'inspection_date',
                            'inspection_type', 'violations', 'location_latitude', 'location_longitude'], axis = 1)
        return train