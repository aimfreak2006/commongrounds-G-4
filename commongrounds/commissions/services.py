from .models import Commission, Job, JobApplication

class CommissionService:
    def create_commission(author,commission_data,jobs_data):
        commission = Commission.objects.create(maker=author, **commission_data)
        commission.save()

        for job_data in jobs_data:
            if (job_data['DELETE']):
                continue

            for field in ('DELETE', 'id', 'commission'):
                job_data.pop(field)

            job = Job.objects.create(commission=commission, **job_data)
            job.save()

    def apply_to_job(applicant, job):
        applications = JobApplication.objects.filter(job=job, applicant=applicant)
        open_manpower = job.manpower_required
        if (open_manpower and not applications):
            job_application = JobApplication.objects.create(applicant=applicant, job=job)
            job_application.save()

    def get_commission_summary(commission):
        ACCEPTED = '1A'
        summary = dict()
        jobs = Job.objects.filter(commission=commission)
        for job in jobs:
            accepted_count = JobApplication.objects.filter(job=job, status=ACCEPTED).count()
            open_manpower = job.manpower_required - accepted_count
            summary[job] = open_manpower

        return summary
    
    def sync_job_status(commission):
        FULL = 'F'
        summary = CommissionService.get_commission_summary(commission)
        for job in summary:
            if (summary[job] == 0):
                job.status = FULL
                job.save()

    def sync_commission_status(commission):
        COMMISSION_FULL = '1F'
        JOB_FULL = 'F'
        CommissionService.sync_job_status(commission)
        jobs = Job.objects.filter(commission=commission)
        are_all_full = True

        for job in jobs:
            is_full = (job.status == JOB_FULL)
            are_all_full = are_all_full and is_full

        if (are_all_full):
            commission.status = COMMISSION_FULL
            commission.save()