package data;

import java.util.*;
import java.util.stream.Collectors;

public class StudentDataBase extends Student{
    private List<Student> studentList;


    public void addStudent(List<Student>newList)
    {
        studentList.addAll(newList);
    }


    public List<Student>getStudentList()
    {
        return studentList;
    }
    public void updateStudent(Student personalId,Student updatedId)
    {
        for(int i=0;i<studentList.size();i++)
        {
            Student temp = studentList.get(i);
            if(temp.getPersonalId().equals(updatedId))
            {
                studentList.set(i,updatedId);
                return;
            }
        }
        System.out.println("Студент з персональним ID:" + personalId + "не знайдено.");
    }
    public List<Student> getStudentsForHighScholarship() {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Введіть індекс групи: ");
        String groupName = scanner.nextLine();
        return studentList.stream()
                .filter(student -> student.getGroup().equals(groupName))
                .filter(student -> student.isSessionpassed())
                .filter(student -> student.getAverageGrade() == 5.0) //
                .collect(Collectors.toList());
    }
    public List<Student> getStudentsForScholarship()
    {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Введіть індекс групи: ");
        String groupName = scanner.nextLine();

        return studentList.stream()
                .filter(student -> student.getGroup().equals(groupName))
                .filter(student -> student.isSessionpassed())
                .filter(student -> student.getAverageGrade() == 4.5 || student.getAverageGrade()==3.0 && student.isCommunityWork()) //
                .collect(Collectors.toList());
    }
    public List<String> getAlphabeticalListWithGradesDistribution() {
        Map<String, Map<Double, Long>> distributionByGroupAndGrade = studentList.stream()
                .collect(Collectors.groupingBy(Student::getGroup,
                        Collectors.groupingBy(Student::getAverageGrade, Collectors.counting())));

        return distributionByGroupAndGrade.entrySet().stream()
                .sorted(Comparator.comparing(Map.Entry::getKey)) // Сортування за групою
                .flatMap(entry -> {
                    String groupName = entry.getKey();
                    Map<Double, Long> gradeDistribution = entry.getValue();

                    return gradeDistribution.entrySet().stream()
                            .sorted(Comparator.comparingDouble(Map.Entry::getKey)) // Сортування за оцінкою
                            .map(gradeEntry -> String.format("%s: Оцінка %.1f - %d студентів",
                                    groupName, gradeEntry.getKey(), gradeEntry.getValue()));
                })
                .collect(Collectors.toList());
    }
    public List<String> getExpulsionList() {
        return studentList.stream()
                .filter(student -> student.getAverageGrade() == 2.0) // Визначте критерії для відрахування
                .map(student -> String.format("%s (%s)", student.getFullName(), student.getPersonalId()))
                .collect(Collectors.toList());
    }

    public List<String> getGroupsWithAverageGrade() {
        Map<String, Double> averageGradeByGroup = studentList.stream()
                .collect(Collectors.groupingBy(Student::getGroup, Collectors.averagingDouble(Student::getAverageGrade)));

        return averageGradeByGroup.entrySet().stream()
                .sorted(Map.Entry.comparingByValue()) // Сортування за середнім балом
                .map(entry -> String.format("%s: Середній бал - %.2f", entry.getKey(), entry.getValue()))
                .collect(Collectors.toList());  
    }




}
