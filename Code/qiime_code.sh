qiime feature-table filter-samples \
  --i-table GMTOL_table.qza \
  --m-metadata-file v4-5.txt \
  --o-filtered-table V4-5_table.qza

qiime taxa barplot \
  --i-table V3-V4-5_table.qza \
  --i-taxonomy GMTOL_taxonomy2.qza \
  --m-metadata-file v3-v4-5.txt \
  --o-visualization v3-v4-taxa-bar-plots.qzv

qiime feature-table merge \
  --i-tables V3-V4-5_table.qza V4-5_table.qza \
  --o-merged-table Full-5_table.qza

qiime feature-table filter-samples \
  --i-table Full-5_table.qza \
  --m-metadata-file Squamata.tsv \
  --o-filtered-table squamata_table.qza

qiime taxa barplot \
  --i-table squamata_table.qza \
  --i-taxonomy GMTOL_taxonomy2.qza \
  --m-metadata-file Squamata.tsv \
  --o-visualization squamata-taxa-bar-plots.qzv

qiime diversity alpha-phylogenetic \
  --i-table Full-5_table.qza \
  --i-phylogeny Jun2_GMTOL_rooted_tree.qza \
  --p-metric faith_pd \
  --o-alpha-diversity faith_total_vector.qza

qiime diversity alpha-group-significance \
  --i-alpha-diversity faith_total_vector.qza \
  --m-metadata-file Full-5.tsv \
  --o-visualization faith_total_significance.qzv

qiime diversity alpha \
  --i-table Full-5_table.qza \
  --p-metric shannon \
  --o-alpha-diversity shannon_total_vector.qza

qiime diversity alpha-group-significance \
  --i-alpha-diversity shannon_total_vector.qza \
  --m-metadata-file Full-5.tsv \
  --o-visualization shannon_total_significance.qzv
