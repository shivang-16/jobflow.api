-- AddForeignKey
ALTER TABLE "Applied_Jobs" ADD CONSTRAINT "Applied_Jobs_jobId_fkey" FOREIGN KEY ("jobId") REFERENCES "Job"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
