# Import necessary packages
import biom
import pandas as pd
import glob
from biom import Table, example_table
from sklearn.preprocessing import StandardScaler

# Import feature table
table = biom.load_table("V3-V4-5_table.biom")

# Import metadata
metadata = pd.read_csv(
    'v3-v4-5.txt',
    sep="\t",
    index_col=0
)

# Create new columns
metadata ['Vertebrate'] = metadata.apply(lambda x: 'Vertebrate' if (x['Phylum'] == 'Chordata') else 'Invertebrate', axis = 1)

# Scale metadata values, focus only on relevant columns
scaler = StandardScaler()
scaled_data = pd.DataFrame(data = scaler.fit_transform(metadata[['Temp_Min','Temp_Mean','Temp_Max','Latitude','Precipitation','ETo','Rel_Hum','Wind']]), 
                           columns = ['Temp_Min','Temp_Mean','Temp_Max','Latitude','Precipitation','ETo','Rel_Hum','Wind'], index = metadata.index)
metadata = pd.concat([scaled_data, metadata['Vertebrate']], axis = 1)
metadata.head()

# Filter table to only include features present in more than 5 samples
prevalence = table.to_dataframe().clip(upper=1).sum(axis=1)
features_to_keep = prevalence[prevalence >= 5].index.tolist()
table_filt = table.filter(features_to_keep, axis="observation")

# Filter table to include features with total counts greater than 5 and samples with total counts greater than 0
table_filt_df = table_filt.to_dataframe()
over_0_s = table_filt_df.sum()>0
over_5_ft = table_filt_df.sum(axis=1)>5
table_filt_df = table_filt_df.loc[over_5_ft,over_0_s]
table_filt_new = Table(table_filt_df.values, table_filt_df.index, table_filt_df.columns)

# Specify default model
from birdman import NegativeBinomial

nb = NegativeBinomial(
     table=table_filt_new,
     formula="Temp_Mean+Temp_Min+Temp_Max+Latitude+Precipitation+ETo+Rel_Hum+Wind+Vertebrate",
     metadata=metadata,
    beta_prior = 0.1
)

# Compile and fit model
nb.compile_model()
nb.fit_model()

# Save model for analysis
from birdman.transform import posterior_alr_to_clr

inference = nb.to_inference()
inference.to_netcdf("v_model.nc")
