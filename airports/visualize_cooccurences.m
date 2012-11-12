close all

fontSize = 7;
fontSizeLabels = 14;

D = dlmread('coocurence.txt', '\t');

fid = fopen('cooccurence_airport_names.txt', 'rt');
labels = textscan(fid, '%s\n', ...
                          'HeaderLines', 0);
                      
figure;
numUsers = zeros(size(D,1),1);
for i=1:size(D,1)
    numUsers(i) = D(i,i);
end
[numUsersSorted idx] = sort(log10(numUsers));
barh(numUsersSorted, 'histc');
set(gca, 'YTick', [1:size(D,1)])
set(gca, 'YTickLabel', labels{1}(idx), 'FontSize', fontSize)
xlabel('log_{10}(Unique users)', 'FontSize', fontSizeLabels)
ylabel('Airports', 'FontSize', fontSizeLabels)
ylim([1 size(D,1)+1])


for i=1:size(D,1)
    D(i,i) = 0;
end

figure;
imagesc(D)
axis square;
set(gca, 'YTick', [1:size(D,1)])
set(gca, 'YTickLabel', labels{1}, 'FontSize', fontSize)
colormap hot
colorbar('location','EastOutside')

