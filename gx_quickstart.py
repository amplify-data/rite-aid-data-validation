import great_expectations as gx

# setup great expectations
context = gx.get_context()

validator = context.sources.pandas_default.read_csv(
    "https://raw.githubusercontent.com/great-expectations/gx_tutorials/main/data/yellow_tripdata_sample_2019-01.csv"
)

# create expectactions
validator.expect_column_values_to_not_be_null(
    column="pickup_datetime"
)

validator.expect_column_mean_to_be_between(
    column="trip_distance", min_value=5, max_value=10
)

validator.expect_column_values_to_be_between(
    column="passenger_count", min_value=1, max_value=6
)

validator.expect_column_values_to_be_between(
    column="fare_amount", min_value=2, max_value=200
)

validator.expect_column_values_to_be_in_set(
    column="store_and_fwd_flag", value_set=["N", "Y"]
)

validator.save_expectation_suite(discard_failed_expectations=False)

my_checkpoint_name = "taxis_checkpoint"

# validate data
checkpoint = context.add_or_update_checkpoint(
    name=my_checkpoint_name,
    validator=validator,
)

# confirm data matches expectations
checkpoint = context.add_or_update_checkpoint(
    name=my_checkpoint_name,
    validator=validator,
)

# create validation results
checkpoint_result = checkpoint.run()
context.view_validation_result(checkpoint_result)