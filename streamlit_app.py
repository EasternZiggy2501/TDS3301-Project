import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from streamlit_folium import folium_static
import folium
from PIL import Image
from apyori import apriori

import warnings
warnings.filterwarnings('ignore')


dataset = pd.read_csv('dataset.csv')
cleaned_dataset = pd.read_csv('cleaned_data.csv')
location_dataset = pd.read_csv('city.csv')
holiday_dataset = pd.read_csv('occasion.csv')
weather_dataset = pd.read_csv('Temperature.csv')
df = pd.read_csv('completed.csv')

# make the streamlit in light mode
st.set_page_config(layout='wide', page_title='TDS3301 Data Mining Project',
                   page_icon=':bar_chart:', initial_sidebar_state='auto')

Image.open('mmu.png').convert('RGB').save('mmu.jpeg')
crb = Image.open('mmu.jpeg')
st.image(crb, width=500)

st.title('TDS3301 Data Mining Project')
st.text('Done by: \n Muhammad Uzair Bin Abdul Razak \t 1191303163 \n Iman Aisyah binti Zailani \t \t 1191302815 \n Nursabrina Binti Zakilfaton \t         1191302411\n Lakshana Kannathal Udaiyappan \t         1201302708')
st.text('\n')
st.text('\n')
st.header('\nExploratory Data Analysis')
st.markdown("Handling null values")

# show the dataset in the streamlit in table format
st.subheader('Provided Dataset')
st.write(dataset)

# show the sum of the null values in the dataset for each column, with the column name says the sum of null values
st.subheader('Sum of null values in each column on the provided dataset')
st.write(dataset.isnull().sum())

st.write('The null values for categorical data type column are filled up with random choices between the existing values in the column')
st.write('For the numerical data type column, the null values are filled up with the mean, median, minimum, and maximum values of the column')

st.subheader('Cleaned Dataset')
st.write(cleaned_dataset)

st.subheader('Sum of null values in each column on the cleaned dataset')
st.write(cleaned_dataset.isnull().sum())

st.subheader('External Dataset Obtain')
st.write('1. Extracting the location city name dataset based latitude and longitude of the given dataset on Streamlit Map')
st.map(cleaned_dataset)
st.write('The locations extracted are with the total of each cities: ')
# show the count of the location in the dataset
st.write(location_dataset['City'].value_counts())

st.write('2. Next is to extract the holiday information based on the date of the given dataset')
st.write(cleaned_dataset['Date'])
st.write('The occassions of holidays extracted are with the total of each cities: ')
# show the count of the location in the dataset
st.write(holiday_dataset['Occasion'].value_counts())

st.write('3. The last external dataset is to extract the weather information based on the date and location of the given dataset\n \t alongside with the temperature and humidity')
cityName = location_dataset.copy()
date = cleaned_dataset['Date']
information = pd.concat([date, cityName], axis=1)
st.write(information)
st.write('The weather information extracted are with the total of each cities: ')
# show the count of the location in the dataset
st.write(weather_dataset)

st.write('Further exploration to know whether certain variables of data are related to another variable of data')
st.write('The variables tchosen are the basket sizes and the number of baskets')
# show images side by side
col1, col2 = st.columns(2)
# convert the images to jpeg format
Image.open('stacked bar.png').convert('RGB').save('stacked bar.jpeg')
Image.open('Anova.png').convert('RGB').save('Anova.jpeg')
# show the images
col1.image('stacked bar.jpeg')
col2.image('Anova.jpeg')
st.write('The results from the Anova test shows that the p-value = 0.730 is greater that the \u03B1 = 0.05, thus show that number of baskets/size of basket do not affect the visitor\'s time spent at the laundry shop')


st.header('\nStart of Data Mining')
st.subheader('\nAssociation Rule Mining')


record = df.copy()
record.drop(['Date', 'Time', 'latitude', 'longitude', 'Temperature', 'Humidity',
             'Washer_No', 'Dryer_No', 'TimeSpent_minutes', 'buyDrinks', 'TotalSpent_RM',
             'Num_of_Baskets', 'Age_Range', 'Pants_Colour', 'Shirt_Colour', 'Basket_colour',
             'Body_Size', 'With_Kids', 'Spectacles', 'Kids_Category', 'Spectacles'], axis=1, inplace=True)

# rearrange columns to obtain the optimal possibilities that are strongly related
weather = record['Weather']
occasions = record['Occasion']
items = record['Wash_Item']
city = record['City']
record.drop(labels=['Weather', 'Occasion',
            'Wash_Item', 'City'], axis=1, inplace=True)

record.insert(0, 'Weather', weather)
record.insert(1, 'City', city)
record.insert(2, 'Occasion', occasions)
record.insert(4, 'Wash_Item', items)

st.write('The dataset used for the association rule mining is: ')
st.write(record)

st.write('The association rule mining is done using the Apriori algorithm')
st.write('The best rules based on the lift of the association rule mining is: ')
st.write('Rule 7: When the weather is just passing cloud, during the Christmas holiday, and when the customer is wearing a traditional attire')
st.write('To prove it, this rule has the highest lift value of 10.2981, confidence of 0.6333, and support of 0.005')
st.write('For a further confirmation of the rule, chi-square test is done to check whether the rule is significant or not')
st.write('By picking the first two condition from the best rule, a study to find the relationship are doe to determine whether this two variables are dependent of each other')

Image.open('chi.png').convert('RGB').save('chi.jpeg')
crb = Image.open('chi.jpeg')
st.image(crb, width=500)

st.write('By understanding the graph H0 is rejected in accordance to the p-value = 8.195e-53 which are lesser than the \u03B1 = 0.05 from the test, showing that weather is related to the occasion have an impact to laundromat business')

st.subheader('\nClustering Analysis')
st.write('The clustering analysis use are the KPrototypes algorithm. This clustering techniques were chosen for it is able to handle both categorical and numerical data type simultaneously for comparison')
st.write('The dataset used are partition between object data type and numerical data type with the target being the weather')
st.write('Therefore, this analysis uses weather as one categorical data type and the rest of the dataset as the numerical data type to study the relation it has with the weather')
st.write(pd.read_csv('weathercluster.csv'))

st.write('The data are then presented in the form of bar chart to tally the frquence of customer goes to the laundromat based on the weather')

Image.open('kproto.png').convert('RGB').save('kproto.jpeg')
crb = Image.open('kproto.jpeg')
st.image(crb, width=500)

st.write('Here in the graph it shows that the frequency of customer goes to the laundromat is higher when the weather is just passing cloud.')

st.write('Simultaneously, the weather data are also being used to understand the relationship between the weather and was item that are being at the time of the visit')
st.write(pd.read_csv('item.csv'))

st.write('Afterwards, the Kprototype algorithm is used to generate an elbow graph to determine the optimal number of clusters')

Image.open('cluster num.png').convert('RGB').save('cluster num.jpeg')
crb = Image.open('cluster num.jpeg')
st.image(crb, width=500)

st.write('The optimal number of clusters is 3 as it is the point where the graph starts to flatten out')
st.write('The number of clusters then are used to segment the data into 3 clusters')
st.write(pd.read_csv('clusterSegment.csv'))

st.write('With the clusters present, it can now be shown in a scatterplot to understand the relationship between the weather, temperature, and humidity')

Image.open('cluster.png').convert('RGB').save('cluster.jpeg')
crb = Image.open('cluster.jpeg')
st.image(crb, width=500)

st.subheader('\nFeature Selection')
st.write('Question: How is a customer\'s Wash Item affect the sales of the laundry shop?')
st.subheader('BORUTA')

Image.open('BORUTA.png').convert('RGB').save('BORUTA.jpeg')
crb = Image.open('BORUTA.jpeg')
st.image(crb, width=500)

st.write('These are the features that are selected by the Boruta algorithm')
st.write('According to Boruta, during the weather is dense fog, humidity and City of Putrajaya & Cyberjaya are the features that contribute the most.')

st.write('The sales of the laundry shop according to customer\'s wash item (either blankets or clothes) depends on weather which is during dense fog, humidity (the lower the temperature, the higher amount of people) and City (highest are Putrajaya & Cyberjaya, maybe because of the distance)')

st.write('RFE')

Image.open('RFE.png').convert('RGB').save('RFE.jpeg')
crb = Image.open('RFE.jpeg')
st.image(crb, width=500)

st.write('These are the features that are selected by the RFE algorithm')
st.write('According to RFE, the presence of kids with the customers at laundry shop can be observed by the Number of Baskets, during specific weather (gloomy/raining/unclear air - Thunderstorms, Passing clouds, Partly cloudy, Dense fog)')

st.subheader('Model Evaluation of Feature Selection')
st.write('The model evaluation of feature selection is done by using Naive Bayes algorithm and Decision Tree algorithm')

col1, col2 = st.columns(2)
# convert the images to jpeg format
Image.open('BORUTAROC.png').convert('RGB').save('BORUTAROC.jpeg')
Image.open('RFEROC.png').convert('RGB').save('RFEROC.jpeg')
# show the images
col1.image('BORUTAROC.jpeg')
col2.image('RFEROC.jpeg')

st.write('Based on the ROC curve, the model evaluation of feature selection using RFE algorithm is better than the BORUTA algorithm')
st.write('Additionally, by utilising Naive Bayes and Decision Tree algorithm, the model shows that the decision tree algorithm is better than the Naive Bayes algorithm')
st.write('After all the mean accuracy from these algorithms are shown:')

st.write('BORUTA Naive Bayes: 50.759')
st.write('BORUTA Decision Tree: 58.934')
st.write('RFE Naive Bayes: 74.208')
st.write('RFE Decision Tree: 73.867')

st.write('In conclusion, RFE algorithm is better than BORUTA algorithm with Decision Tree algorithm is better than Naive Bayes algorithm')

st.subheader('Classification Model')
st.write('The classification model is done by using Naive Bayes Classifier, kNN Classifier, and Random Forest Classifier')
st.write('Three of these classification model are used to predict which gender of customer frequently visits the laundry shop')

st.write('Throughout the testing of these three classification model results are shown in the table below:')

st.write('Naive Bayes Classifier: 100%')
st.write('Random Forest Classifier: 100%')
st.write('kNN Classifier: 97%')

st.write('This shows that kNN Classifier is not a good classification model to predict using this dataset')

st.subheader('Regression Model')

st.subheader('Linear Regression')
st.write('The linear regression model is to look at weather if it affects the time spent by the customer in the laundry shop')

Image.open('Linear Regression.png').convert(
    'RGB').save('Linear Regression.jpeg')
crb = Image.open('Linear Regression.jpeg')
st.image(crb, width=500)

st.write('The linear regression model shows that the time spent by the customer in the laundry shop does not shows any association')
st.write('Therefore, we can conclude that the weather does not affect the time spent by the customer in the laundry shop')

st.subheader('Logistic Regression')
st.write('As for the logictic regression model, it is to predict the whether during holidays or normal business day, do customers brought along their kids to the laundry shop')

Image.open('logR.png').convert('RGB').save('logR.jpeg')
crb = Image.open('logR.jpeg')
st.image(crb, width=500)

st.write('As shown in the bar graph above, the number of customers who brought their kids to the laundry shop is higher during the holidays, expecially on Christmas')
st.write('Additionally, the accuracy of the model is 67%')
