/*
  Warnings:

  - The `about` column on the `Company` table would be dropped and recreated. This will lead to data loss if there is data in the column.

*/
-- AlterTable
ALTER TABLE "Company" ADD COLUMN     "description" TEXT,
DROP COLUMN "about",
ADD COLUMN     "about" JSONB;
