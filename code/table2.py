'''
Concentration metric:
For each predictor, take the top k% patients in terms of predicted risk.

including standard errors
SE = SD where SD = sqrt(p(1-p) / n) where n is the entire holdout
SD of a proportion (aka fraction)
reference: https://stattrek.com/estimation/standard-error.aspx
'''
import pandas as pd
import os
import model.util as util


def get_concentration_metric_df(k, holdout_pred_df,
                                y_predictors=['log_cost_t',
                                              'log_cost_avoidable_t',
                                              'gagne_sum_t'],
                                outcomes=['log_cost_t', 'log_cost_avoidable_t',
                                          'gagne_sum_t', 'dem_race_black']):
    OUTCOME_DICT = {
        'cost_t': 'Total costs',
        'log_cost_t': 'Total costs',
        'cost_avoidable_t': 'Avoidable costs',
        'log_cost_avoidable_t': 'Avoidable costs',
        'gagne_sum_t': 'Active chronic conditions',
        'dem_race_black': 'Race black'
    }

    top_n = int(k * len(holdout_pred_df))
    all_concentration_metric = []

    for y_col in y_predictors:
        y_hat_col = '{}_hat'.format(y_col)
        y_hat_percentile_col = '{}_hat_percentile'.format(y_col)
        # sort by y_hat_col
        top_n_df = holdout_pred_df.sort_values(by=y_hat_col, ascending=False).iloc[:top_n]
        concentration_dict = {
            'predictor': OUTCOME_DICT[y_col]
        }

        for outcome in outcomes:
            if 'log_' in outcome:
                # for the outcomes presented on a log scale,
                # we sum the un-logged values.
                outcome = outcome[len('log_'):]
            top_n_outcome = top_n_df[outcome].sum()
            if outcome == 'dem_race_black':
                total_outcome = top_n
            else:
                total_outcome = holdout_pred_df[outcome].sum()

            # calculate concentration metric
            frac_top_n = top_n_outcome / total_outcome

            # save to concentration_dict
            concentration_dict[OUTCOME_DICT[outcome]] = frac_top_n

            n = len(holdout_pred_df)
            import math
            # SD = sqrt[ p*(1-p) / n]
            standard_deviation = math.sqrt((frac_top_n * (1-frac_top_n))/n)

            # save to concentration dict
            concentration_dict[OUTCOME_DICT[outcome] + ' SE'] = standard_deviation
        all_concentration_metric.append(concentration_dict)

    concentration_df = pd.DataFrame(all_concentration_metric)
    concentration_df = concentration_df.set_index('predictor')
    # define column order
    column_order = []
    for outcome in outcomes:
        outcome = OUTCOME_DICT[outcome]
        column_order.append(outcome)
        column_order.append(outcome + ' SE')
    return concentration_df[column_order]


def get_best_worst_difference(df):
    # add 'best - worst difference'
    best_worst_dict = {
        'predictor': 'Best-worst difference'
    }
    for col in df.columns:
        if 'SE' == col[-2:]:
            continue
        min = df[col].min()
        max = df[col].max()
        diff = max - min
        best_worst_dict[col] = diff
    best_worst_row = pd.DataFrame(best_worst_dict, index=[0]).set_index('predictor')
    return best_worst_row


def build_table2():
    # define output dir
    git_dir = util.get_git_dir()
    OUTPUT_DIR = util.create_dir(os.path.join(git_dir, 'results'))

    # load holdout predictions
    holdout_pred_fp = os.path.join(OUTPUT_DIR, 'model_lasso_predictors.csv')
    holdout_pred_df = pd.read_csv(holdout_pred_fp)

    k = 0.03
    concentration_df = get_concentration_metric_df(k, holdout_pred_df)
    best_worst_row = get_best_worst_difference(concentration_df)

    table2 = pd.concat([concentration_df, best_worst_row], sort=False)

    # save output to CSV
    filename = 'table2_concentration_metric.csv'
    output_filepath = os.path.join(OUTPUT_DIR, filename)
    print('...writing to {}'.format(output_filepath))
    table2.to_csv(output_filepath, index=True)

if __name__ == '__main__':
    build_table2()
