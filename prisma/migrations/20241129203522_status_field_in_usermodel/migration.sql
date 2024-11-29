-- CreateEnum
CREATE TYPE "UserStatus" AS ENUM ('BOOKMARKED', 'APPLIED', 'ACCEPTED', 'REJECTED');

-- AlterTable
ALTER TABLE "User" ADD COLUMN     "status" TEXT[] DEFAULT ARRAY['bookmarked', 'applied', 'accepted', 'rejected']::TEXT[];
