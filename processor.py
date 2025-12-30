import logging
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
import time

# Professional Logging: Helps us see which thread is doing which work
logging.basicConfig(level=logging.INFO, format='%(threadName)s: %(message)s')

class DataProcessor(ABC):
    """Abstract Base Class defining the blueprint for data transformation."""
    @abstractmethod
    def transform(self, row):
        pass

class DataTransformation(DataProcessor):
    """Specific implementation to simulate complex data cleaning."""
    def transform(self, row):
        try:
            # Simulate a 10% tax calculation or similar logic
            row['value'] = float(row['value']) * 1.10
            return row
        except (ValueError, KeyError):
            logging.error(f"Data corruption detected in row: {row}")
            return None

class ProcessingEngine:
    """The High-Performance Engine using Multi-threading."""
    def __init__(self, processor: DataProcessor, max_workers=4):
        self.processor = processor
        self.max_workers = max_workers

    def run_parallel(self, data):
        """Splits data into chunks and processes them across multiple workers."""
        # Calculate chunk sizes based on number of workers
        chunk_size = max(1, len(data) // self.max_workers)
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

        start_time = time.time()

        # This is where the magic happens: Parallel execution
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Each worker thread takes one chunk of the data
            final_results = list(executor.map(self.process_batch, chunks))

        duration = time.time() - start_time
        logging.info(f"Parallel Task Completed in {duration:.4f} seconds.")

        # Flatten the results from all threads into one list
        return [item for sublist in final_results for item in sublist]

    def process_batch(self, batch):
        """Helper method: Processes chunk while ensuring transformation only happens once."""
        results = []
        for row in batch:
            transformed = self.processor.transform(row)
            if transformed is not None:
                results.append(transformed)
        return results