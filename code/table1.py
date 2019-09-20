"""
Build table1.
"""
import pandas as pd
import os
import model.util as util


def get_table1(df, race, total_n):
    df = df.copy()
    table1_list = []  # list of tuples

    n = len(df)*1.0
    table1_list.append(('n (patient-years)', '{:,}'.format(n)))

    # Demographics
    table1_list.append(('Demographics', '---'))
    table1_list.append(('Age 18-24', '{:.2f}'.format(df['dem_age_band_18-24'].sum() / n)))
    table1_list.append(('Age 25-34', '{:.2f}'.format(df['dem_age_band_25-34'].sum() / n)))
    table1_list.append(('Age 35-44', '{:.2f}'.format(df['dem_age_band_35-44'].sum() / n)))
    table1_list.append(('Age 45-54', '{:.2f}'.format(df['dem_age_band_45-54'].sum() / n)))
    table1_list.append(('Age 55-64', '{:.2f}'.format(df['dem_age_band_55-64'].sum() / n)))
    table1_list.append(('Age 65-74', '{:.2f}'.format(df['dem_age_band_65-74'].sum() / n)))
    table1_list.append(('Age 75+', '{:.2f}'.format(df['dem_age_band_75+'].sum() / n)))
    table1_list.append(('Female', '{:.2f}'.format(df['dem_female'].sum() / n)))

    # Care management program
    table1_list.append(('Care management program', '---'))
    df['risk_score_t_percentile'] = util.assign_percentile(df, 'risk_score_t').astype(int)
    table1_list.append(('Algorithm score (percentile)', '{:.0f}'.format(df['risk_score_t_percentile'].mean())))
    table1_list.append(('Race composition of program (%)', '{:.1f}'.format(n / total_n * 100)))

    # Care utilization
    table1_list.append(('Care utilization', '---'))
    table1_list.append(('Actual cost', '${:,.0f}'.format(df['cost_t'].mean())))

    # Mean biomarker values
    table1_list.append(('Mean biomarkers', '---'))
    table1_list.append(('HbA1c', '{:.1f}'.format(df['ghba1c_mean_t'].mean())))
    table1_list.append(('Systolic BP', '{:.1f}'.format(df['bps_mean_t'].mean())))
    table1_list.append(('Creatinine', '{:.1f}'.format(df['cre_mean_t'].mean())))
    table1_list.append(('Hematocrit', '{:.1f}'.format(df['hct_mean_t'].mean())))
    table1_list.append(('LDL', '{:.1f}'.format(df['ldl_mean_t'].mean())))


    # Active chronic illnesses (comorbidities)
    table1_list.append(('Active chronic illnesses (comorbidities)', '---'))
    table1_list.append(('Total number of active illnesses', '{:.2f}'.format(df['gagne_sum_t'].mean())))
    table1_list.append(('Hypertension', '{:.2f}'.format(df['hypertension_elixhauser'].mean())))
    table1_list.append(('Diabetes, uncomplicated', '{:.2f}'.format(df['uncompdiabetes_elixhauser'].mean())))
    table1_list.append(('Arrythmia', '{:.2f}'.format(df['arrhythmia_elixhauser'].mean())))
    table1_list.append(('Hypothyroid', '{:.2f}'.format(df['hypothyroid_elixhauser'].mean())))
    table1_list.append(('Obesity', '{:.2f}'.format(df['obesity_elixhauser'].mean())))
    table1_list.append(('Pulmonary disease', '{:.2f}'.format(df['pulmonarydz_romano'].mean())))
    table1_list.append(('Cancer', '{:.2f}'.format(df['tumor_romano'].mean())))
    table1_list.append(('Depression', '{:.2f}'.format(df['depression_elixhauser'].mean())))
    table1_list.append(('Anemia', '{:.2f}'.format(df['anemia_elixhauser'].mean())))
    table1_list.append(('Arthritis', '{:.2f}'.format(df['arthritis_elixhauser'].mean())))
    table1_list.append(('Renal failure', '{:.2f}'.format(df['renal_elixhauser'].mean())))
    table1_list.append(('Electrolyte disorder', '{:.2f}'.format(df['electrolytes_elixhauser'].mean())))
    table1_list.append(('Heart failure', '{:.2f}'.format(df['chf_romano'].mean())))
    table1_list.append(('Psychosis', '{:.2f}'.format(df['psychosis_elixhauser'].mean())))
    table1_list.append(('Valvular disease', '{:.2f}'.format(df['valvulardz_elixhauser'].mean())))
    table1_list.append(('Stroke', '{:.2f}'.format(df['hemiplegia_romano'].mean())))
    table1_list.append(('Peripheral vascular disease', '{:.2f}'.format(df['pvd_elixhauser'].mean())))
    table1_list.append(('Diabetes, complicated', '{:.2f}'.format(df['compdiabetes_elixhauser'].mean())))
    table1_list.append(('Heart attack', '{:.2f}'.format(df['myocardialinfarct_romano'].mean())))
    table1_list.append(('Liver disease', '{:.2f}'.format(df['liver_elixhauser'].mean())))

    table1_df = pd.DataFrame(table1_list, columns=['Descriptive stats', race])

    return table1_df

def build_table1():
    # define output dir
    git_dir = util.get_git_dir()
    OUTPUT_DIR = util.create_dir(os.path.join(git_dir, 'results'))

    # load data file
    data_fp = os.path.join(git_dir, 'data' ,'data_new.csv')
    data_df = pd.read_csv(data_fp)

    total_n = len(data_df)*1.0

    # split by white, black patients
    white_df = data_df[data_df['race'] == 'white']
    black_df = data_df[data_df['race'] == 'black']

    white_table1 = get_table1(white_df, 'White', total_n)
    black_table1 = get_table1(black_df, 'Black', total_n)

    table1 =  white_table1.merge(black_table1)

    # save to CSV
    filename = 'table1.csv'
    output_filepath = os.path.join(OUTPUT_DIR, filename)
    print('...writing to {}'.format(output_filepath))
    table1.to_csv(output_filepath, index=False)

if __name__ == '__main__':
    build_table1()
