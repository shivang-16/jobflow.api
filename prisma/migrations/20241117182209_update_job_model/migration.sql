/*
  Warnings:

  - Made the column `job_type` on table `Job` required. This step will fail if there are existing NULL values in that column.

*/
-- AlterTable
ALTER TABLE "Job" ADD COLUMN     "company_link" TEXT,
ALTER COLUMN "job_location" DROP NOT NULL,
ALTER COLUMN "job_type" SET NOT NULL;
