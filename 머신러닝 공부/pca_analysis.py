from sklearn.decomposition impor PCA
pca=PCA(n_components=2).fit()
print("Projected feature on Eigen space\n%s"%pca.transform(std_group)[:5])
print("Projected feature on Eigen space\n%s"%pca.components_)
print("Projected feature on Eigen space\n%s"%sum(pca.explained_variance_ratio_)
