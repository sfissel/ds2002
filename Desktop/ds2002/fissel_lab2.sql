#1) Find the number of Male (M) and Female (F) employees in the database and order the counts in descending order.
SELECT gender, COUNT(*) 
FROM employees 
GROUP BY gender
ORDER BY COUNT(*) DESC;
#2) Find the average salary by employee title, round to 2 decimal places and order by descending order. HINT: You’ll use ROUND, AVG, GROUP BY and ORDER BY
SELECT titles.title, ROUND(AVG(salaries.salary), 2)
FROM titles
INNER JOIN salaries ON titles.emp_no=salaries.emp_no
GROUP BY titles.title
ORDER BY ROUND(AVG(salaries.salary), 2) DESC;
#3) Find all the employees that have worked in at least 2 departments. Show their first name, last_name and the number of departments they work in. Display all results in ascending order. HINT JOIN on emp_no
SELECT employees.first_name, employees.last_name, COUNT(dept_emp.dept_no)
FROM employees
INNER JOIN dept_emp ON employees.emp_no=dept_emp.emp_no
GROUP BY employees.first_name, employees.last_name
HAVING COUNT(dept_emp.dept_no)>=2
ORDER BY COUNT(dept_emp.dept_no) ASC;
#4) Display the first name, last name, and salary of the highest paid employee.
SELECT employees.first_name, employees.last_name, salaries.salary
FROM employees
INNER JOIN salaries ON employees.emp_no=salaries.emp_no
ORDER BY salaries.salary DESC LIMIT 1;
#5) Display the first name, last name, and salary of the second highest paid employee.
SELECT employees.first_name, employees.last_name, salaries.salary
FROM employees
INNER JOIN salaries ON employees.emp_no=salaries.emp_no
ORDER BY salaries.salary DESC LIMIT 1,1;
#6) Display the month and total hires for the month with the most hires.
SELECT MONTH(hire_date), COUNT(hire_date)
FROM employees
GROUP BY MONTH(hire_date)
ORDER BY COUNT(hire_date) DESC LIMIT 1;
#7) Display each department and the age of the youngest employee at hire date. HINT: You’ll join on emp_no and dept_no
SELECT departments.dept_name, YEAR(employees.hire_date)-YEAR(employees.birth_date)
FROM ((dept_emp
INNER JOIN employees ON dept_emp.emp_no=employees.emp_no)
INNER JOIN departments ON dept_emp.dept_no=departments.dept_no)
GROUP BY departments.dept_name, YEAR(employees.hire_date)-YEAR(employees.birth_date)
ORDER BY YEAR(employees.hire_date)-YEAR(employees.birth_date) ASC LIMIT 9;
#8) Find all the employees that do not contain vowels in their first name and display the department they work in.
SELECT employees.first_name, employees.last_name, departments.dept_name
FROM ((dept_emp
INNER JOIN employees ON dept_emp.emp_no=employees.emp_no)
INNER JOIN departments ON dept_emp.dept_no=departments.dept_no)
WHERE employees.first_name NOT LIKE '%A%'  
	AND employees.first_name  NOT LIKE '%E%'  
    AND employees.first_name NOT LIKE '%I%'  
    AND employees.first_name NOT LIKE '%O%'  
    AND employees.first_name NOT LIKE '%U%';