# Day-2: Document Annotation Task

## Overview

This task focused on annotating fillable fields in document forms collected from the Tennessee Real Estate Commission (TREC) forms repository. The objective was to create high-quality annotations for machine learning and document understanding purposes.

## Task Description

Annotated documents from the following categories:

* Applicants Forms
* Licensees Forms
* Firms Forms

The annotation process involved identifying and labeling various fillable fields present in the documents while maintaining consistency throughout the dataset.

## Annotation Requirements Followed

* Annotated all available documents provided for the task.
* Ensured bounding boxes tightly fit the target fields.
* Maintained consistent labeling across the dataset.
* Avoided missing any visible fillable fields.
* Reviewed annotations before exporting the dataset.

## Labels Used

The following annotation classes were used:

* checkbox
* free_text
* date
* signature
* initial
* phone_number
* email
* address

### Label Descriptions

| Label        | Description                                   |
| ------------ | --------------------------------------------- |
| checkbox     | Selectable check boxes such as Yes/No options |
| free_text    | General text input fields                     |
| date         | Date entry fields                             |
| signature    | Signature areas                               |
| initial      | Initial signature fields                      |
| phone_number | Phone number fields                           |
| email        | Email address fields                          |
| address      | Address-related fields                        |

## Deliverables

The following files have been included in this folder:

1. Annotation Export File
2. Annotation Screenshots
3. Research Report
4. README.md

## Types of Fields Identified

During annotation, the following field types were identified:

* Text Input Fields
* Checkboxes
* Date Fields
* Signature Fields
* Initial Fields
* Phone Number Fields
* Email Fields
* Address Fields

## Challenges Faced

* Distinguishing between free_text and specialized fields.
* Identifying fields with unclear boundaries.
* Maintaining consistent annotations across multiple forms.
* Handling forms with different layouts and formatting styles.

## Lessons Learned

* Importance of consistent labeling for machine learning datasets.
* Proper bounding box placement improves dataset quality.
* Understanding document structure is essential for accurate annotation.
* Reviewing annotations helps reduce labeling errors.

## Confusing Scenarios

Some fields required careful examination, including:

* Differentiating free_text fields from address fields.
* Identifying signature versus initial fields.
* Determining whether Yes/No options should be labeled as checkboxes.
* Handling fields with overlapping labels and instructions.

## Research Conducted

### Concepts Learned

* Document Annotation
* Object Detection
* Bounding Boxes
* Dataset Creation
* COCO Annotation Format
* Data Labeling Best Practices
* Annotation Consistency
* Computer Vision Dataset Preparation

### Resources Used

* Roboflow Documentation
* COCO Dataset Documentation
* Machine Learning and Computer Vision Tutorials
* Tennessee Real Estate Commission Forms
* Internal Internship Guidelines and Instructions

## Annotation Workflow

1. Downloaded document forms.
2. Uploaded documents to annotation platform.
3. Created annotation classes.
4. Annotated fillable fields.
5. Reviewed annotations for quality assurance.
6. Exported dataset in COCO format.
7. Organized deliverables and uploaded to GitHub.

## Summary

This task provided hands-on experience in document annotation and dataset preparation. The project improved understanding of object detection datasets, annotation standards, and the importance of consistent labeling for machine learning applications.
