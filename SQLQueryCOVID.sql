-- Highest deaths by country on the latest date of measurement
select location, max(date) as latest, sum(total_deaths) as deaths_by_country
from Covid_Data.dbo.CovidDeaths
where location not in ('World', 'Europe', 'North America', 'Asia', 'Africa', 'South America', 'European Union')
group by location
order by deaths_by_country desc

-- Mortality per country on the last day of measurement
select location, date, total_deaths, total_cases, mortality
from(
	select location, date,total_deaths,total_cases,(CAST(total_deaths as float) / nullif(cast(total_cases as float), 0) * 100) as mortality,
	ROW_NUMBER() over(partition by location order by date desc) as rn
	from Covid_Data.dbo.CovidDeaths) as x
where x.rn = 1 and location <> ' ' and location not in ('World', 'Europe', 'North America', 'Asia', 'Africa', 'South America', 'European Union')

-- Highest every mortality in each country
select location, max((cast(total_deaths as float) / nullif(cast(total_cases as float), 0) * 100)) as mortality
from Covid_Data.dbo.CovidDeaths
where location not in ('World', 'Europe', 'North America', 'Asia', 'Africa', 'South America', 'European Union', ' ')
group by location, total_deaths, total_cases
order by mortality

-- Highest infection rate
select location, population, max(total_cases) as Highest_Inf, max((cast(total_cases as float) / nullif(cast(population as float), 0) * 100)) as Infection_rate
from Covid_Data.dbo.CovidDeaths
where location not in ('World', 'Europe', 'North America', 'Asia', 'Africa', 'South America', 'European Union','International', ' ')
group by location, population
order by Infection_rate desc

-- Highest death count
select location, population, max(total_deaths) as Highest_Death, max((cast(total_deaths as float) / nullif(cast(population as float), 0) * 100)) as Death_rate
from Covid_Data.dbo.CovidDeaths
where continent <> ' '
group by location, population
order by Death_rate desc

-- Total deatch count by continent
select continent, max(total_deaths) as Death_count
from Covid_Data.dbo.CovidDeaths
where continent <> ' '
group by continent
order by Death_count desc

-- global development over time
select date, sum(new_cases) as global_cases, sum(new_deaths) as global_deaths, (sum(cast(new_deaths as float))/nullif(sum(cast(new_cases as float)), 0)*100) as mortality
from Covid_Data.dbo.CovidDeaths
where continent <> ' '
group by date
order by date

-- joining the two tables
select *
from Covid_Data.dbo.CovidDeaths as a
inner join Covid_Data.dbo.CovidVaccinations as b
	on a.location = b.location and a.date = b.date

-- total population vs vaccinations
select a.continent, a.location, a.date,a.population, b.new_vaccinations
from Covid_Data.dbo.CovidDeaths as a
inner join Covid_Data.dbo.CovidVaccinations as b
	on a.location = b.location and a.date = b.date
where a.continent <> ' '

-- rolling sum of vaccinations per country
select a.continent, a.location, a.date,a.population, b.new_vaccinations,
sum(b.new_vaccinations) over(partition by a.location order by a.location, a.date) as rolling_sum
from Covid_Data.dbo.CovidDeaths as a
inner join Covid_Data.dbo.CovidVaccinations as b
	on a.location = b.location and a.date = b.date
where a.continent <> ' '
order by a.location, a.date

--CTE for rolling sum
with vacc as (
select a.continent, a.location, a.date,a.population, b.new_vaccinations,
sum(b.new_vaccinations) over(partition by a.location order by a.location, a.date) as rolling_sum
from Covid_Data.dbo.CovidDeaths as a
inner join Covid_Data.dbo.CovidVaccinations as b
	on a.location = b.location and a.date = b.date
where a.continent <> ' '
)
select *, (cast(rolling_sum as float)/nullif(cast(population as float), 0)* 100) as vacc_in_population
from vacc

-- Create temporary table
drop table if exists #Percentage_of_Vacc
create table #Percentage_of_Vacc (
    Continent NVARCHAR(255),
    Location NVARCHAR(255),
    Date DATETIME,
    New_Vaccinations NUMERIC,
    Rolling_sum NUMERIC
);

insert into #Percentage_of_Vacc (Continent, Location, Date, New_Vaccinations, Rolling_sum)
select 
    a.continent, 
    a.location, 
    a.date, 
    coalesce(b.new_vaccinations, 0) as New_Vaccinations,
    sum(coalesce(b.new_vaccinations, 0)) over (partition by a.location order by a.date) as Rolling_sum
from Covid_Data.dbo.CovidDeaths as a
inner join Covid_Data.dbo.CovidVaccinations as b
    on a.location = b.location 
    and a.date = b.date
where a.continent is not null and a.continent <> '';  

select * from #Percentage_of_Vacc

-- Creating a view
create view Percentage_of_Vacc as
select a.continent, a.location, a.date,a.population, b.new_vaccinations,
SUM(b.new_vaccinations) over(partition by a.location order by a.location, a.date) as rolling_sum
from Covid_Data.dbo.CovidDeaths as a
inner join Covid_Data.dbo.CovidVaccinations as b
	on a.location = b.location and a.date = b.date
where a.continent <> ' '
