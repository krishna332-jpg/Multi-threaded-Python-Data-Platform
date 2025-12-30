from processor import DataTransformation, ProcessingEngine

def main():
    # 1. Simulate a large dataset (e.g., 10,000 rows of employee data)
    # Each 'value' represents a salary or a data point to be transformed
    raw_data = [{'id': i, 'name': f'User_{i}', 'value': 1000} for i in range(10000)]

    # 2. Add some "malformed" data to test our error handling
    raw_data.append({'id': 99999, 'name': 'Corrupt_User', 'value': 'not_a_number'})

    print(f"--- Starting Data Pipeline with {len(raw_data)} records ---")

    # 3. Initialize our components
    # We use 4 workers (threads) to process the data simultaneously
    transformer = DataTransformation()
    engine = ProcessingEngine(processor=transformer, max_workers=4)

    # 4. Run the parallel engine
    processed_results = engine.run_parallel(raw_data)

    # 5. Output summary
    print(f"--- Pipeline Finished ---")
    print(f"Successfully processed: {len(processed_results)} records.")
    print(f"Sample Result: {processed_results[0]}")

if __name__ == "__main__":
    main()