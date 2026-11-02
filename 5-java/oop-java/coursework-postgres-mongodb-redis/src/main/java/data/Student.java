package data;

public class Student {
    private int studentId;
    private String personalId;
    private String fullName;
    private int course;
    private String specializationCode;
    private double averageGrade;
    private int participationInActivities;
    private double successRate;
    private int numberOfExams;
    private boolean dormitoryResidence;
    private boolean sessionpassed;
    private String group;
    private boolean communityWork;
    private int group_id;
    public Student()
    {

    }
    public Student(int studentId,String personalId,String fullName,int course,String specializationCode,double averageGrade
    ,int participationInActivities,double successRate,int numberOfExams,boolean dormitoryResidence,boolean sessionpassed,
                   String group,boolean communityWork,int group_id)
    {
        this.studentId=studentId;
        this.personalId=personalId;
        this.fullName=fullName;
        this.course=course;
        this.specializationCode=specializationCode;
        this.averageGrade=averageGrade;
        this.participationInActivities=participationInActivities;
        this.successRate=successRate;
        this.numberOfExams=numberOfExams;
        this.dormitoryResidence=dormitoryResidence;
        this.sessionpassed=sessionpassed;
        this.group=group;
        this.communityWork=communityWork;
        this.group_id=group_id;
    }
    public String getGroup()
    {
        return group;
    }

    public boolean isCommunityWork() {
        return communityWork;
    }

    public int getGroup_id() {
        return group_id;
    }

    public boolean isSessionpassed() {
        return sessionpassed;
    }

    public int getStudentId()
    {
        return studentId;
    }
    public int getCourse()
    {
        return course;
    }
    public int getParticipationInActivities()
    {
        return participationInActivities;
    }
    public int getNumberOfExams()
    {
        return numberOfExams;
    }
    public double getAverageGrade()
    {
        return averageGrade;
    }
    public double getSuccessRate()
    {
        return successRate;
    }
    public String getPersonalId()
    {
        return personalId;
    }
    public String getFullName()
    {
        return fullName;
    }

    public void setCommunityWork(boolean communityWork) {
        this.communityWork = communityWork;
    }

    public String getSpecializationCode()
    {
        return specializationCode;
    }
    public boolean getDormitoryResidence()
    {
        return dormitoryResidence;
    }

    public void setGroup(String group) {
        this.group = group;
    }

    public void setAverageGrade(double averageGrade) {
        this.averageGrade = averageGrade;
    }

    public void setCourse(int course) {
        this.course = course;
    }

    public void setDormitoryResidence(boolean dormitoryResidence) {
        this.dormitoryResidence = dormitoryResidence;
    }

    public void setSessionpassed(boolean sessionpassed) {
        this.sessionpassed = sessionpassed;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
    }

    public void setNumberOfExams(int numberOfExams) {
        this.numberOfExams = numberOfExams;
    }

    public void setParticipationInActivities(int participationInActivities) {
        this.participationInActivities = participationInActivities;
    }
    public void setGroup_id(int group_id)
    {
        this.group_id=group_id;
    }

    public void setStudentId(int studentId) {
        this.studentId = studentId;
    }

    public void setPersonalId(String personalId) {
        this.personalId = personalId;
    }

    public void setSpecializationCode(String specializationCode) {
        this.specializationCode = specializationCode;
    }

    public void setSuccessRate(double successRate) {
        this.successRate = successRate;
    }
}
