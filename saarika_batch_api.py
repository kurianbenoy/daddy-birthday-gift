import logging
from sarvamai import SarvamAI, SpeechToTextJobParametersParams

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def main():
    # Initialize sync client
    client = SarvamAI(api_subscription_key="")
    logging.info("Initialized SarvamAI client.")

    # Create job
    job = client.speech_to_text_job.create_job(
        job_parameters=SpeechToTextJobParametersParams(
            language_code="hi-IN",
            model="saarika:v2.5",
        )
    )
    logging.info(f"Created job with ID: {job.job_id}")

    # Upload audio files
    audio_paths = [
        "/Users/vinayakgavariya/Downloads/audio.wav",
        "/Users/vinayakgavariya/Downloads/arjun-kannada.wav",
    ]
    job.upload_files(file_paths=audio_paths)
    logging.info("All files uploaded successfully.")

    # Start job
    job.start()
    logging.info(f"Started processing for job ID: {job.job_id}")

    # Wait for job to complete
    final_status = job.wait_until_complete()
    logging.info(f"Final job status: {final_status.job_state}")

    # job.is_successful and job.is_failed
    if job.is_failed():
        logging.error("STT job failed.")
        return

    # Download outputs
    output_dir = "./out"
    job.download_outputs(output_dir=output_dir)
    logging.info(f"All output files downloaded to: {output_dir}")


if __name__ == "__main__":
    main()
